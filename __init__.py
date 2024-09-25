"""
__init__.py

This module initializes the Flask application with its configurations, 
database setup, session management, and other necessary integrations.
"""

from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from redis import Redis
from flask_session import Session
from flask_bcrypt import Bcrypt

# Create an instance of the Flask app
app = Flask(__name__, static_url_path='/static', static_folder='static')

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Load environmental variables from the .env file
load_dotenv()

# Get environmental variables for database connection
DELIVER_MYSQL_HOST = os.environ.get('DELIVER_MYSQL_HOST')
DELIVER_MYSQL_DB = os.environ.get('DELIVER_MYSQL_DB')
DELIVER_MYSQL_USER = os.environ.get('DELIVER_MYSQL_USER')
DELIVER_MYSQL_PWD = os.environ.get('DELIVER_MYSQL_PWD')
DELIVER_MYSQL_ENV = os.environ.get('DELIVER_MYSQL_ENV')
DELIVER_MYSQL_PORT = os.environ.get('DELIVER_MYSQL_PORT')

# Set up the secret key for signing sessions
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Setup MySQL server URI
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mysql://{DELIVER_MYSQL_USER}:{DELIVER_MYSQL_PWD}@{DELIVER_MYSQL_HOST}:{DELIVER_MYSQL_PORT}/{DELIVER_MYSQL_DB}'
)

# Session configuration using Redis
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = Redis(host='localhost', port=6379)
REDIS = app.config['SESSION_REDIS']

# Configure session expiry date to 1 day
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Initialize the session management
Session(app)

# Instantiate the SQLAlchemy database
db = SQLAlchemy(app)

# Set up migration for database updates
migrate = Migrate(app, db)

# Configure file upload settings
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']

# Limit the size of file uploads
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000  # 16 MB

# Create the upload folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    """
    Check if a file is allowed based on its extension.

    Args:
        filename (str): The name of the file to check.

    Returns:
        bool: True if the file extension is allowed, False otherwise.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create all database tables
with app.app_context():
    db.create_all()

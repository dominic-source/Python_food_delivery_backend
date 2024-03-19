from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_server.views.v1 import app_views
app = Flask(__name__)
app.register_blueprint(app_views)

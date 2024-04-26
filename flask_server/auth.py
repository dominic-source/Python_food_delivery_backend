"""
This module is used to authenticate users, and also authorize
users to be able to carryout some task
"""
from flask import session, request
from flask_server import bcrypt, db
from flask_server.models import User
import uuid
import datetime

class Auth():
    """The authentication class"""
    models_major = ['User', 'Product', 'Payment', 'Order', 'OrderItem', 'Location']
    models_minor = ['Category', 'Lga', 'State', 'Country']
    
    def login_user(self) -> bool:
        """Login a user"""
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        if email is None or password is None:
            return False
        user = db.session.query(User).filter_by(email=email).one()
        if not user:
            return False
        if bcrypt.check_password_hash(user.password_hash, password):
            if session.get('user_id', None):
                return True
            session['user_id'] = user.id
            return True
        return False
    
    def logout_user(self) -> bool:
        """Logout a user"""
        if session.get('user_id', None):
            try:
                session.pop('user_id')
            except Exception:
                return False
            return True
        elif not session.get('user_id', None):
            return True

    def is_authorized(self, model) -> bool:
        """Authorize a user to have certain abilities"""
        if model not in Auth.models_major or model not in Auth.models_minor:
            return False
        if model in Auth.models_minor and (request.method == 'DELETE' or
                               request.method == 'UPDATE' or
                               request.method == 'PUT' or
                               request.method == 'POST'):
            return False
        return True

    def is_logged_in(self):
        """Check if user is logged in"""
        if session.get('user_id', None):
            return True
        return False

    def forgot_password(self) -> str:
        """Helper function, to change a users password"""
        email = request.form.get('email')
        if not email:
            return ''
        expiry = datetime.datetime.now() + datetime.timedelta(days=1)
        user = db.session.query(User).filter_by(email=email).one()
        if not user:
            return ''
        token = str(uuid.uuid4()) + str(uuid.uuid4())
        user.reset_password_token = token + '  ' + str(expiry)
        db.session.commit()
        return token
    
    def update_password(self) -> bool:
        """updates a users password"""
        token = request.form.get('token')
        email = request.form.get('email')
        user = db.session.query(User).filter_by(email=email).one()
        if not user:
            return False
        reset = user.reset_password_token.split('  ')
        if reset[0] != token:
            return False
        expire = datetime.datetime.strptime(reset[1], '%Y-%m-%d %H:%M:%S.%f')
        if expire < datetime.datetime.now():
            return False
        password = request.form.get('password')
        user.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        db.session.commit()
        return True
auth = Auth()

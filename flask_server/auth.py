"""
This module is used to authenticate users, and also authorize
users to be able to carryout some task
"""
from flask import session, request
from flask_server import bcrypt, db
from flask_server.models import User


class Auth():
    """The authentication class"""
    models_major = ['User', 'Product', 'Payment', 'Order', 'OrderItem', 'Location']
    models_minor = ['Category', 'Lga', 'State', 'Country']
    def login_user(username:str=None, password:str=None) -> bool:
        """Login a user"""
        if username is None or password is None or id is None:
            return False
        user = db.session.query(User).filter_by(username=username).one()
        if not user:
            return False
        if bcrypt.check_password_hash(user.password_hash, password):
            if session.get('user_id', None):
                return True
            session['user_id'] = user.id
            return True
    
    def logout_user() -> bool:
        """Logout a user"""
        if session.get('user_id', None):
            try:
                session.pop('user_id')
            except Exception:
                return False
            return True
        if not session.get('user_id', None):
            return True

    def isAuthorized(model) -> bool:
        """Authorize a user to have certain abilities"""
        if model not in Auth.models_major or model not in Auth.models_minor:
            return False
        if model in Auth.models_minor and (request.method == 'DELETE' or
                               request.method == 'UPDATE' or
                               request.method == 'PUT' or
                               request.method == 'POST'):
            return False
    def isLogin():
        """Check if user is logged in"""
        if session.get('user_id', None):
            return True
        return False

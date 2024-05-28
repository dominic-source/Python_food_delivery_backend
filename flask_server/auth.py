"""
auth.py

This module handles user authentication and authorization tasks.
It provides functionalities for logging in, logging out, checking 
if a user is an admin, managing forgotten passwords, and updating passwords.
"""

from flask import session, request
from flask_server import bcrypt, db, REDIS
from flask_server.models import User
import uuid
import datetime
import json
from flask_server.views.v1 import logger

class Auth:
    """The authentication class"""

    def is_admin(self) -> bool:
        """
        Confirms if the user is an administrator.

        Returns:
            bool: True if the user is an administrator, False otherwise.
        """
        user_id = session.get('user_id', None)
        if not user_id:
            return False
        try:
            user = User.query.filter_by(id=user_id).one()
            if user.username != 'admin' or user.email != 'admin@deliver.com':
                return False
            return True
        except Exception:
            return False

    def login_user(self) -> bool:
        """
        Log in a user.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        try:
            if email is None or password is None:
                return False
            user = db.session.query(User).filter_by(email=email).first()
            if not user:
                return False
            if bcrypt.check_password_hash(user.password_hash, password):
                if session.get('user_id', None):
                    return True
                session['user_id'] = user.id
                return True
        except Exception:
            return False
    
    def logout_user(self) -> bool:
        """
        Log out a user.

        Returns:
            bool: True if logout is successful, False otherwise.
        """
        if session.get('user_id', None):
            try:
                session.pop('user_id')
            except Exception:
                logger.info('An invalid user attempted to logout')
                return False
            return True
        elif not session.get('user_id', None):
            return True

    def is_logged_in(self) -> bool:
        """
        Check if user is logged in.

        Returns:
            bool: True if the user is logged in, False otherwise.
        """
        if session.get('user_id', None):
            return True
        return False

    def forgot_password(self) -> bool:
        """
        Helper function to change a user's password.

        Returns:
            bool: A reset token if successful, False otherwise.
        """
        email = request.form.get('email')
        if not email:
            return False
        expiry = datetime.datetime.now() + datetime.timedelta(hours=1)
        try:
            user = db.session.query(User).filter_by(email=email).one()
            if not user:
                return False
            token = str(uuid.uuid4()) + str(uuid.uuid4())
            user.reset_password_token = token + '  ' + str(expiry)
            db.session.commit()
            message = token
            redis = REDIS
            user_data = {
                "id": user.id,
                "subj": 'password update',
                "mess": message,
                "sen": "chinonsodomnic@gmail.com", 
                "rec": email, 
                "pas": None
            }
            data = json.dumps(user_data)
            redis.rpush('user_data_queue', data)
            return token
        except Exception:
            logger.error("Error occurred:", exc_info=True)
            db.session.rollback()
            return False

    def update_password(self) -> bool:
        """
        Update a user's password.

        Returns:
            bool: True if the password update is successful, False otherwise.
        """
        token = request.form.get('token')
        email = request.form.get('email')
        try:
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
        except Exception:
            logger.error("Error occurred:", exc_info=True)
            db.session.rollback()
            return False

# Create an instance of the Auth class
auth = Auth()

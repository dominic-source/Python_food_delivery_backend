#!/usr/bin/python3
"""This module is used to manage our blueprints
"""
from flask import Blueprint
import logging
from functools import wraps


logger = logging.getLogger(__name__)
# Configure logging
logging.basicConfig(filename='consumer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def protected_route(func):
    """Decorator that ensures a route is protected"""
    @wraps(func)
    def protect(*args, **kwargs):
        if not auth.is_logged_in():
            return jsonify({'error': 'An error occured, try to log in!'}), 403
        return func(*args, **kwargs)
    return protect


app_views = Blueprint('app_views', __name__, url_prefix='/api')
from flask_server.views.v1.user import *
from flask_server.views.v1.category import *
from flask_server.views.v1.product import *

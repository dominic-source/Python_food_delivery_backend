#!/usr/bin/python3
"""
__init__.py

This module is used to manage our blueprints and define decorators
for route protection and administration checks.
"""

from flask import Blueprint, jsonify
import logging
from functools import wraps
from flask_server.auth import auth  # Assuming auth is imported correctly

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='consumer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def admin_route(func: callable) -> callable:
    """
    A decorator that allows only admin to access a particular route.

    Args:
        func (callable): The function to decorate.

    Returns:
        callable: The decorated function.
    """
    @wraps(func)
    def admin(*args, **kwargs):
        if not auth.is_admin():
            return jsonify({'error': 'You need to be an admin to access this route!'}), 403
        return func(*args, **kwargs)
    return admin


def protected_route(func: callable) -> callable:
    """
    A decorator that ensures a route is protected.

    Args:
        func (callable): The function to decorate.

    Returns:
        callable: The decorated function.
    """
    @wraps(func)
    def protect(*args, **kwargs):
        if not auth.is_logged_in():
            return jsonify({'error': 'An error occurred, try to log in!'}), 403
        return func(*args, **kwargs)
    return protect


def generate_orders(order: list) -> list:
    """
    Generates a list of orders with specific attributes.

    Args:
        order (list): A list of order objects.

    Returns:
        list: A list of dictionaries representing orders.
    """
    if not order:
        return []
    return [{
            'id': order_b.id,
            'buyer_id': order_b.buyer_id,
            'seller_id': order_b.seller_id,
            'dispatcher_id': order_b.dispatcher_id,
            'date_of_order': order_b.order_date_time,
            'currency': order_b.currency,
            'total_amount': order_b.total_amount,
            'status': order_b.status,
            'delivery_address': order_b.delivery_address,
            } for order_b in order]

# Create a Blueprint for the application views
app_views = Blueprint('app_views', __name__, url_prefix='/api')

# Import all necessary modules to register routes
from flask_server.views.v1.user import *
from flask_server.views.v1.category import *
from flask_server.views.v1.product import *
from flask_server.views.v1.order import *
from flask_server.views.v1.payment import *

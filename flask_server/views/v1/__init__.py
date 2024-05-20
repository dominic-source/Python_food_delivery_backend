#!/usr/bin/python3
"""This module is used to manage our blueprints
"""
from flask import Blueprint
import logging
from functools import wraps


logger = logging.getLogger(__name__)
# Configure logging
logging.basicConfig(filename='consumer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def admin_route(func):
    """A decorator that allows only admin to access a particular route"""
    @wraps(func)
    def admin(*args, **kwargs):
        if not auth.is_admin():
            return jsonify({'error': 'You need to be an admin to access this route!'}), 403
        return func(*args, **kwargs)
    return admin


def protected_route(func):
    """Decorator that ensures a route is protected"""
    @wraps(func)
    def protect(*args, **kwargs):
        if not auth.is_logged_in():
            return jsonify({'error': 'An error occured, try to log in!'}), 403
        return func(*args, **kwargs)
    return protect


def generate_orders(order):
    if not order:
        return []
    return [{
            'id': order_b.id,
            'buyer_id': order_b.buyer_id,
            'seller_id': order_b.seller_id,
            'dispatcher_id': order_b.dispatcher_id,
            'date_of _order': order_b.order_date_time,
            'currency': order_b.currency,
            'total_amount': order_b.total_amount,
            'status': order_b.status,
            'delivery_address': order_b.delivery_address,
            } for order_b in order]


app_views = Blueprint('app_views', __name__, url_prefix='/api')
from flask_server.views.v1.user import *
from flask_server.views.v1.category import *
from flask_server.views.v1.product import *
from flask_server.views.v1.order import *

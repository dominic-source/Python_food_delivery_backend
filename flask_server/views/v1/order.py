""" This module is used to manage the orders
"""
import json
from flask_server.views.v1 import app_views, protected_route, logger
from flask import request, jsonify, make_response, session
from flask_server.models import Product, Category, User, Order, OrderItem
from flask_server import db
from datetime import datetime


@app_views.route('/order', methods=['POST'], strict_slashes=False)
@protected_route
def create_order():
    """This endpoint retrieves all usersproducts"""
    try:
        if request.is_json is False:
            return jsonify({'error': 'This route requires you use json'}), 401
        request_data = json.loads(request.json)
        seller_id = request_data.get('seller_id')
        buyer_id = session.get('user_id')
        dispatcher_id = request_data.get('dispatcher_id')
        delivery_address = request_data.get('delivery_address')
        orderitems = request_data.get('orderitems')
        # verify if the seller exist or not
        seller = User.query.filter_by(id=seller_id).first()
        if not seller:
            return jsonify({'error': 'seller not found!'}), 401
        if not dispatcher_id:
            return jsonify({'error': 'dispatcher not found!'}), 401
        # verify if the dispatcher exist or not
        dispatcher = User.query.filter_by(id=dispatcher_id).first()
        if not dispatcher:
            return jsonify({'error': 'dispatcher not found!'}), 401
        order_n = Order(seller_id=seller_id, buyer_id=buyer_id, dispatcher_id=dispatcher_id, delivery_address=delivery_address)
        total_amount = 0
        currency = None
        for data in orderitems:
            product_id = data['product_id']
            quantity = data['quantity']
            product = Product.query.filter_by(id=product_id).first()
            currency = product.currency
            if not product:
                return jsonify({'error': 'product not found!'}), 401
            total_amount += product.price * quantity
            item = OrderItem(order_id=order_n.id, product_id=product_id, quantity=quantity)
            order_n.orderitems.append(item)

        order_n.currency = currency
        order_n.total_amount = total_amount
        db.session.add(order_n)
        db.session.commit()
        return jsonify({'order_id': order_n.id}), 201
    except Exception as e:
        print(e)
        db.session.rollback()
        logger.error("Error occured:", exc_info=True)
        return jsonify({'error': 'An error occured!'}), 401

""" This module is used to manage the orders
"""
import json
from flask_server.views.v1 import app_views, protected_route, logger, admin_route, generate_orders
from flask import request, jsonify, make_response, session
from flask_server.models import Product, Category, User, Order, OrderItem
from flask_server import db
import datetime
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional, Tuple


@app_views.route('/order/<int:order_id>', methods=['PUT'], strict_slashes=False)
@protected_route
def update_order_items(order_id: Optional[int] = None) -> Tuple[dict, int]:
    """
    This endpoint updates an order item from an order.

    Args:
        order_id (int, optional): The ID of the order to update.

    Returns:
        Tuple[dict, int]: A tuple containing a JSON response and a status code.
        The JSON response contains a success message or an error message.

    Raises:
        HTTPException: 400 (Bad Request) if the order ID is not provided or if an order item does not belong to the order,
                       403 (Forbidden) if the user is not authorized to update the order or if the order has already been paid,
                       404 (Not Found) if the order or an order item does not exist,
                       415 (Unsupported Media Type) if the request is not JSON,
                       500 (Internal Server Error) if an error occurs during update.
    """
    try:
        user_id = session.get('user_id')
        if not order_id:
            return jsonify({'error': 'Order ID is required'}), 400

        if not request.is_json:
            return jsonify({'error': 'This route requires JSON input'}), 415

        request_data = request.get_json()
        orderitems = request_data.get('orderitems')

        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        if not (order.buyer_id == user_id or order.seller_id == user_id):
            return jsonify({'error': 'Unauthorized transaction'}), 403

        if order.payment and order.payment.payment_status == 'paid':
            return jsonify({'error': 'Order has already been paid'}), 403

        for data in orderitems:
            item_id = data.get('id')
            orderitem = OrderItem.query.get(item_id)
            if not orderitem:
                return jsonify({'error': 'Order item not found'}), 404
            if order_id != orderitem.order_id:
                return jsonify({'error': 'Order item does not belong to this order'}), 400

            quantity = data.get('quantity')
            orderitem.quantity = quantity

        # Update the order total amount
        total_amount = 0
        for item in order.orderitems:
            product = Product.query.get(item.product_id)
            total_amount += item.quantity * product.price
        order.total_amount = total_amount
        db.session.commit()

        return jsonify({'message': 'Order item was updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An internal error occurred'}), 500


@app_views.route('/order/<int:order_id>/<int:orderitem_id>', methods=['DELETE'], strict_slashes=False)
@protected_route
def delete_an_order_item(order_id: Optional[int] = None, orderitem_id: Optional[int] = None) -> Tuple[dict, int]:
    """
    This endpoint deletes an order item from an order.

    Args:
        order_id (int, optional): The ID of the order.
        orderitem_id (int, optional): The ID of the order item to delete.

    Returns:
        Tuple[dict, int]: A tuple containing a JSON response and a status code.
        The JSON response contains a success message or an error message.

    Raises:
        HTTPException: 400 (Bad Request) if the order ID or order item ID is not provided or if an order item does not belong to the order,
                       403 (Forbidden) if the user is not authorized to delete the order item or if the order has already been paid or is in process of payment,
                       404 (Not Found) if the order or the order item does not exist,
                       500 (Internal Server Error) if an error occurs during deletion.
    """
    try:
        user_id = session.get('user_id')
        if not order_id:
            return jsonify({'error': 'Order ID is required'}), 400
        if not orderitem_id:
            return jsonify({'error': 'Order item ID is required'}), 400

        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        if not (order.buyer_id == user_id or order.seller_id == user_id):
            return jsonify({'error': 'Unauthorized transaction'}), 403
        if order.payment and order.payment.payment_status == 'paid':
            return jsonify({'error': 'Order has already been paid'}), 403
        if order.payment and order.payment.payment_status == 'inprocess':
            if order.payment.last_update_time > (datetime.datetime.now() - datetime.timedelta(minutes=60)):
                return jsonify({'error': 'Order is in process of payment'}), 403

        orderitem = OrderItem.query.get(orderitem_id)
        if not orderitem:
            return jsonify({'error': 'Order item not found'}), 404
        if orderitem.order_id != order_id:
            return jsonify({'error': 'Order item does not belong to this order'}), 400

        db.session.delete(orderitem)
        db.session.commit()

        return jsonify({'message': 'Order item was deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An internal error occurred'}), 500


@app_views.route('/order/<int:order_id>', methods=['DELETE'], strict_slashes=False)
@protected_route
def delete_order(order_id: Optional[int] = None) -> Tuple[dict, int]:
    """
    This endpoint deletes an order.

    Args:
        order_id (int, optional): The ID of the order to delete.

    Returns:
        Tuple[dict, int]: A tuple containing a JSON response and a status code.
        The JSON response contains a success message or an error message.

    Raises:
        HTTPException: 400 (Bad Request) if the order ID is not provided,
                       403 (Forbidden) if the user is not authorized to delete the order or if the order has already been paid or is in process of payment,
                       404 (Not Found) if the order does not exist,
                       500 (Internal Server Error) if an error occurs during deletion.
    """
    try:
        user_id = session.get('user_id')
        if not order_id:
            return jsonify({'error': 'Order ID is required'}), 400

        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        if not (order.buyer_id == user_id or order.seller_id == user_id):
            return jsonify({'error': 'Unauthorized transaction'}), 403
        if order.payment and order.payment.payment_status == 'paid':
            return jsonify({'error': 'Order has already been paid'}), 403
        if order.payment and order.payment.payment_status == 'inprocess':
            if order.payment.last_update_time > (datetime.datetime.now() - datetime.timedelta(minutes=60)):
                return jsonify({'error': 'Order is in process of payment'}), 403

        db.session.delete(order)
        db.session.commit()

        return jsonify({'message': 'Order was deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An internal error occurred'}), 500


@app_views.route('/order', methods=['PUT'], strict_slashes=False)
@protected_route
def update_order_address() -> Tuple[dict, int]:
    """
    This endpoint updates an order's address.

    Args:
        order_id (int, mandatory): The ID of the order to update.
        delivery_address (str, optional): The delivery address of the order.

    Returns:
        Tuple[dict, int]: A tuple containing a JSON response and a status code.
        The JSON response contains a success message or an error message.

    Raises:
        HTTPException: 400 (Bad Request) if the order ID is not provided or is not a valid integer,
                       403 (Forbidden) if the user is not authorized to update the order,
                       404 (Not Found) if the order does not exist,
                       500 (Internal Server Error) if an error occurs during update.
    """
    try:
        user_id = session.get('user_id')
        order_id = request.form.get('order_id')
        delivery_address = request.form.get('delivery_address')

        if not order_id or not order_id.isdigit():
            return jsonify({'error': 'Valid order ID is required'}), 400

        order_id = int(order_id)
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        if order.buyer_id != user_id:
            return jsonify({'error': 'Unauthorized transaction'}), 403

        if delivery_address:
            order.delivery_address = delivery_address
            order.last_update_time = datetime.datetime.now()

        db.session.commit()

        return jsonify({'message': 'Order updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An internal error occurred'}), 500


@app_views.route('/order_items/<id>', methods=['GET'], strict_slashes=False)
@protected_route
def get_all_items_of_order(id: Optional[str] = None) -> Tuple[dict, int]:
    """
    This endpoint retrieves all the items associated with an order.

    To access this endpoint, your user ID must be either a seller, buyer,
    or dispatcher associated with the order.

    Args:
        id (str, optional): The ID of the order to retrieve items for.

    Returns:
        Tuple[dict, int]: A tuple containing a JSON response and a status code.
        The JSON response contains the order items or an error message.

    Raises:
        HTTPException: 400 (Bad Request) if the order ID is missing,
                       404 (Not Found) if the order is not found,
                       500 (Internal Server Error) if an error occurs during retrieval.
    """
    try:
        if id is None or not id.isdigit():
            return jsonify({'error': 'Valid order ID is required'}), 400

        user_id = session.get('user_id')

        # Filter based on user role and provided ID
        query = Order.query.filter(
            (Order.seller_id == user_id) |
            (Order.buyer_id == user_id) |
            (Order.dispatcher_id == user_id)
        ).filter_by(id=int(id))

        orderitems = query.one().orderitems
        items = [{ 
            'id': order.id,
            'product_id': order.product_id,
            'quantity': order.quantity} for order in orderitems]
        return jsonify(items), 200

    except NoResultFound:
        return jsonify({'error': 'Order not found'}), 404

    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An internal error occurred!'}), 500


@app_views.route('/all_orders', methods=['GET'], strict_slashes=False)
@admin_route
@protected_route
def get_all_order() -> Tuple[dict, int]:
    """
    This endpoint retrieves all orders. It is accessible only to admins.

    Returns:
        Tuple[dict, int]: A tuple containing a JSON response and a status code.
        The JSON response contains all the orders or an error message.

    Raises:
        HTTPException: 500 (Internal Server Error) if an error occurs during retrieval.
    """
    try:
        orders = Order.query.all()
        return jsonify(generate_orders(orders)), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An internal error occurred!'}), 500


@app_views.route('/my_orders', methods=['GET'], strict_slashes=False)
@protected_route
def get_my_orders() -> Tuple[dict, int]:
    """
    This endpoint returns all the user's orders as a buyer, seller, and/or dispatcher.

    Args:
        seller (str, optional): If 'true', returns orders where the user is the seller.
        buyer (str, optional): If 'true', returns orders where the user is the buyer.
        dispatcher (str, optional): If 'true', returns orders where the user is the dispatcher.

    Returns:
        Tuple[dict, int]: A tuple containing a JSON response and a status code.
        The JSON response contains the orders or an error message.

    Raises:
        HTTPException: 500 (Internal Server Error) if an error occurs during retrieval.
    """
    seller = request.args.get('seller', 'false')
    buyer = request.args.get('buyer', 'false')
    dispatcher = request.args.get('dispatcher', 'false')
    data = {}
    try:
        id = session.get('user_id')
        if buyer.lower() == 'true':
            order_b = Order.query.filter_by(buyer_id=id).all()
            data['buyer'] = generate_orders(order_b)
        if seller.lower() == 'true':
            order_s = Order.query.filter_by(seller_id=id).all()
            data['seller'] = generate_orders(order_s)
        if dispatcher.lower() == 'true':
            order_d = Order.query.filter_by(dispatcher_id=id).all()
            data['dispatcher'] = generate_orders(order_d)
        return jsonify(data), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An internal error occurred!'}), 500


@app_views.route('/order', methods=['POST'], strict_slashes=False)
@protected_route
def create_order() -> Tuple[dict, int]:
    """
    This endpoint creates a new order.

    The request data should include 'seller_id', 'dispatcher_id', 'delivery_address', and 'orderitems'.
    'orderitems' should be a list of dictionaries, each containing 'product_id' and 'quantity'.

    Returns:
        Tuple[dict, int]: A tuple containing a JSON response and a status code.
        The JSON response contains the ID of the created order or an error message.

    Raises:
        HTTPException: 401 (Unauthorized) if the request is not JSON,
                       if the seller or dispatcher does not exist,
                       or if a product does not exist.
                       500 (Internal Server Error) if an error occurs during creation.
    """
    try:
        if not request.is_json:
            return jsonify({'error': 'This route requires you use json'}), 401

        request_data = request.get_json()
        seller_id = request_data.get('seller_id')
        buyer_id = session.get('user_id')
        dispatcher_id = request_data.get('dispatcher_id')
        delivery_address = request_data.get('delivery_address')
        orderitems = request_data.get('orderitems')

        seller = User.query.get(seller_id)
        if not seller:
            return jsonify({'error': 'Seller not found'}), 401

        dispatcher = User.query.get(dispatcher_id)
        if not dispatcher:
            return jsonify({'error': 'Dispatcher not found'}), 401

        order_n = Order(seller_id=seller_id, buyer_id=buyer_id, dispatcher_id=dispatcher_id, delivery_address=delivery_address)
        total_amount = 0
        currency = None

        for data in orderitems:
            product_id = data['product_id']
            quantity = data['quantity']
            product = Product.query.get(product_id)
            if not product:
                return jsonify({'error': 'Product not found'}), 401

            total_amount += product.price * quantity
            item = OrderItem(order_id=order_n.id, product_id=product_id, quantity=quantity)
            order_n.orderitems.append(item)
            currency = product.currency

        order_n.currency = currency
        order_n.total_amount = total_amount
        db.session.add(order_n)
        db.session.commit()

        return jsonify({'order_id': order_n.id}), 201

    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An internal error occurred!'}), 500

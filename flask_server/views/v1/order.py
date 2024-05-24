""" This module is used to manage the orders
"""
import json
from flask_server.views.v1 import app_views, protected_route, logger, admin_route, generate_orders
from flask import request, jsonify, make_response, session
from flask_server.models import Product, Category, User, Order, OrderItem
from flask_server import db
import datetime
from sqlalchemy.orm.exc import NoResultFound

@app_views.route('/order/<int:order_id>', methods=['PUT'], strict_slashes=False)
@protected_route
def update_order_items(order_id=None):
    """This endpoint deletes an order item from an order.
    Here is the format for the json input: 
        data = {
                'orderitems': [
                    {
                        'id': 1,
                        'quantity': 40
                    },
                    {
                        'id': 2,
                        'quantity': 10
                    }
                ]
            }
    """
    try:
        user_id = session.get('user_id')
        if not order_id:
            return jsonify({'message': 'order id required!'}), 401

        if request.is_json is False:
            return jsonify({'error': 'This route requires you use json'}), 401
        request_data = json.loads(request.json)
        orderitems = request_data.get('orderitems')
        order = Order.query.filter_by(id=order_id).first()
        if not order:
            return jsonify({'message': 'order not found!'}), 401
        if not (order.buyer_id == user_id or order.seller_id == user_id):
            return jsonify({'message': 'you are not the buyer or seller in the transaction!'}), 401
        if order.payment and order.payment.payment_status == 'paid':
            return jsonify({'message': 'order has been paid!'}), 401

        for data in orderitems:
            item_id = data.get('id')
            orderitem = OrderItem.query.filter_by(id=item_id).first()
            if not orderitem:
                return jsonify({'message': 'order item not found!'}), 401
            if order_id != orderitem.order_id:
                return jsonify({'message': 'order item not found!'}), 401
            quantity = data.get('quantity')
            orderitem.quantity = quantity

        # Update the order total amount
        total_amount = 0
        for item in order.orderitems:
            product = Product.query.filter_by(id=item.product_id).first()
            total_amount += item.quantity * product.price
        order.total_amount = total_amount
        db.session.commit()
        return jsonify({'message': 'order item was updated successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An error occurred!'}), 401


@app_views.route('/order/<int:order_id>/<int:orderitem_id>', methods=['DELETE'], strict_slashes=False)
@protected_route
def delete_an_order_item(order_id=None, orderitem_id=None):
    """This endpoint deletes an order item from an order.
    """
    try:
        user_id = session.get('user_id')
        if not order_id:
            return jsonify({'message': 'order id required!'}), 401
        if not orderitem_id:
            return jsonify({'message': 'order item id required!'}), 401
        order = Order.query.filter_by(id=order_id).first()
        if not order:
            return jsonify({'message': 'order not found!'}), 401
        if not (order.buyer_id == user_id or order.seller_id == user_id):
            return jsonify({'message': 'you are not the buyer or seller in the transaction!'}), 401
        if order.payment and order.payment.payment_status == 'paid':
            return jsonify({'message': 'order has been paid!'}), 401
        if order.payment and order.payment.payment_status == 'inprocess':
            if order.payment.last_update_time > (datetime.datetime.now() - datetime.timedelta(minutes=60)):
                return jsonify({'message': 'order in process of payment!'}), 401
        orderitem = OrderItem.query.filter_by(id=orderitem_id).first()
        if not orderitem:
            return jsonify({'message': 'order item not found!'}), 401
        if orderitem.order_id != order_id:
            return jsonify({'message': 'order item not found!'}), 401

        db.session.delete(orderitem)
        db.session.commit()
        return jsonify({'message': 'order item was deleted successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An error occurred!'}), 401


@app_views.route('/order/<int:id>', methods=['DELETE'], strict_slashes=False)
@protected_route
def delete_order(id=None):
    """Delete an order"""
    try:
        user_id = session.get('user_id')
        if not id:
            return jsonify({'message': 'order id required'}), 401
        order = Order.query.filter_by(id=id).first()
        if not order:
            return jsonify({'message': 'order not found!'}), 401
        if not (order.buyer_id == user_id or order.seller_id == user_id):
            return jsonify({'message': 'you are not the buyer or seller in the transaction'}), 401
        if order.payment and order.payment.payment_status == 'paid':
            return jsonify({'message': 'order has been paid!'}), 401
        if order.payment and order.payment.payment_status == 'inprocess':
            if order.payment.last_update_time > (datetime.datetime.now() - datetime.timedelta(minutes=60)):
                return jsonify({'message': 'order in process of payment!'}), 401
        db.session.delete(order)
        db.session.commit()
        return jsonify({'message': 'order deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An error occurred!'}), 401


@app_views.route('/order', methods=['PUT'], strict_slashes=False)
@protected_route
def update_order_address():
    """This endpoint updates an orders address

    endpoint: /order
        You can only update an order if you are the buyer in the transaction
    
    Request content-type: form/encoded

    Request body:
        order_id (int, mandatory): The ID of the order to update.
        delivery_address: The delivery address of the order.

    Returns:
        JSON: A JSON response containing a message of success or failure
    """
    try:
        user_id = session.get('user_id')
        order_id = request.form.get('order_id')
        delivery_address = request.form.get('delivery_address')
        if not order_id:
            return jsonify({'error': 'order id required'}), 401
        order = Order.query.filter_by(id=order_id).first()
        if not order:
            return jsonify({'error': 'order not found!'}), 401
        if order.buyer_id != user_id:
            return jsonify({'error': 'you are not the buyer in the transaction'}), 401
        if delivery_address:
            order.delivery_address = delivery_address
            order.last_update_time = datetime.datetime.now()
        db.session.commit()
        return jsonify({'message': 'order updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occured:", exc_info=True)
        return jsonify({'error': 'An error occured!'}), 401


@app_views.route('/order_items/<id>', methods=['GET'], strict_slashes=False)
@protected_route
def get_all_items_of_order(id=None):
    """This endpoint gets all the items associated with an order.

    To access this endpoint, your user ID must be either a seller, buyer,
    or dispatcher associated with the order.

    Args:
        id (int, mandatory): The ID of the order to retrieve items for.

    Returns:
        JSON: A JSON response containing the order items or an error message.

    Raises:
        HTTPException: 401 (Unauthorized) if the order ID is missing,
                       or an error occurs during retrieval.
    """

    try:
        if id is None:
            return jsonify({'error': 'order id required'}), 401

        user_id = session.get('user_id')

        # Filter based on user role and provided ID
        query = Order.query.filter(
            (Order.seller_id == user_id) |
            (Order.buyer_id == user_id) |
            (Order.dispatcher_id == user_id)
        ).filter_by(id=id)

        orderitems = query.one().orderitems
        items = [{ 
            'id': order.id,
            'product_id': order.product_id,
            'quantity': order.quantity} for order in orderitems]
        return jsonify(items)

    except NoResultFound:
        return jsonify({'error': 'Order not found'}), 404

    except Exception as e:
        db.session.rollback()
        logger.error("Error occured:", exc_info=True)
        return jsonify({'error': 'An error occured!'}), 401


@app_views.route('/all_orders', methods=['GET'], strict_slashes=False)
@admin_route
@protected_route
def get_all_order():
    """This route is an admin route to get all orders"""
    try:
        orders = Order.query.all()
        return jsonify(generate_orders(orders)) 
    except Exception as e:
        db.session.rollback()
        logger.error("Error occured:", exc_info=True)
        return jsonify({'error': 'An error occured!'}), 401


@app_views.route('/my_orders', methods=['GET'], strict_slashes=False)
@protected_route
def get_my_orders():
    """This route returns all the users order as a buyer and/or seller and/or dispatcher
        endpoint: my_orders

        request arguments'/api/my_orders?seller=false&buyer=true&dispatcher=false':
            seller: true | false
            buyer: true | false
            dispatcher: true | false
    """
    seller = request.args.get('seller', 'false')
    buyer = request.args.get('buyer', 'false')
    dispatcher = request.args.get('dispatcher', 'false')
    data = {}
    try:
        id = session.get('user_id')
        if buyer.lower() == 'true':
            order_b = Order.query.filter_by(buyer_id=id).all()
            data['buyer'] =  generate_orders(order_b)
        if seller.lower() == 'true':
            order_s = Order.query.filter_by(seller_id=id).all()
            data['seller'] =  generate_orders(order_s)
        if dispatcher.lower() == 'true':
            order_d = Order.query.filter_by(dispatcher_id=id).all()
            data['dispatcher'] = generate_orders(order_d)
        return jsonify(data), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occured:", exc_info=True)
        return jsonify({'error': 'An error occured!'}), 401


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
        db.session.rollback()
        logger.error("Error occured:", exc_info=True)
        return jsonify({'error': 'An error occured!'}), 401

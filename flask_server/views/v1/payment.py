""" This module is used for to manage the categories
"""
from flask_server.views.v1 import app_views, protected_route, logger
from flask import request, jsonify, make_response, session
from flask_server.models import Order, Payment
from flask_server import db
from datetime import datetime


@app_views.route('/payment/<int:id>', methods=['PUT'], strict_slashes=False)
@protected_route
def update_payment(id=None):
    """"This endpoint will update the payment"""
    try:
        if not id:
            return jsonify({'error': 'Payment Id is required!'}), 401
        status = request.form.get('status', None)
        if not status:
            return jsonify({'error': 'Payment status is required!'}), 401
        payment = Payment.query.filter_by(id=id).one()
        order_id = payment.order_id
        user_id = session.get('user_id')
        order = Order.query.filter_by(id=order_id).one()
        if order.seller_id == user_id:
            payment.seller_payment_status = status
            payment.dispatcher_payment_status = status
        else:
            return jsonify({'message': 'You may not be the seller!'}), 401
        if payment.seller_payment_status == 'paid':
            order.status = 'completed'
        elif payment.seller_payment_status == 'inprocess':
            order.status = 'incomplete'
        else:
            return jsonify({'message': 'An error occurred in your input'}), 401      
        
        payment.payment_date_time = datetime.now()
        payment.last_update_time = datetime.now()
        
        db.session.commit()
        return jsonify({'message': 'Payment has been updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        logger.error("Error occured:", exc_info=True)
        return jsonify({'error': 'An error occured!'}), 401


@app_views.route('/payment', methods=['POST'], strict_slashes=False)
@protected_route
def create_payment():
    """This endpoint will delete a category"""
    try:
        payment_method = request.form.get('payment_method', None)
        seller_amount = request.form.get('seller_amount', None)
        dispatcher_amount = request.form.get('dispatcher_amount', None)
        currency = request.form.get('currency', None)
        order_id = request.form.get('order_id', None)

        user_id=session.get('user_id')
        order = Order.query.filter_by(id=order_id).one()
        if order.buyer_id != user_id:
            return jsonify({'message': 'You are not the buyer!'});
            
        payment = Payment(payment_method=payment_method,
                         seller_amount=seller_amount,
                         dispatcher_amount=dispatcher_amount,
                         currency=currency,
                         order_id=order_id
                         )
        order.payment.append(payment)
        db.session.add(payment)
        db.session.commit()
        return jsonify({'message': 'Payment has been created successfully'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occured:", exc_info=True)
        return jsonify({'error': 'An error occured!'}), 401


@app_views.route('/payments/<int:order_id>', methods=['GET'], strict_slashes=False)
@protected_route
def get_my_payments(order_id=None):
    """This endpoint will get my payments based on my order id"""
    try:
        if not order_id:
            return jsonify({'error': 'Order Id is required!'}), 401
        user_id = session.get('user_id')
        query = Order.query.filter(
            (Order.seller_id == user_id) |
            (Order.buyer_id == user_id) |
            (Order.dispatcher_id == user_id)
            ).filter_by(id=order_id).one()
        payments = query.payment
        if not payments:
            return jsonify({'message': 'No payment was found!'}), 401
        transaction = [{
            'Id': payment.id,
            'Currency': payment.currency,
            'Payment_method': payment.payment_method,
            'Payment_status': payment.seller_payment_status,
            'Date': payment.last_update_time,
            'Amount': (payment.seller_amount + payment.dispatcher_amount) if query.seller_id == user_id or
                                                query.buyer_id == user_id else payment.dispatcher_amount
            } for payment in payments]            
        return jsonify(transaction), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        logger.error("Error occured:", exc_info=True)
        return jsonify({'error': 'An error occured!'}), 401

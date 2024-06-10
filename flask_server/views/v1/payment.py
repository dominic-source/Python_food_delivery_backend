""" This module is used for to manage the categories
"""
from flask_server.views.v1 import app_views, protected_route, logger
from flask import request, jsonify, make_response, session
from flask_server.models import Order, Payment
from flask_server import db
from datetime import datetime
from typing import Optional, Tuple


@app_views.route('/payment/<int:id>', methods=['PUT'], strict_slashes=False)
@protected_route
def update_payment(id=None):
    """
    This endpoint updates a payment.

    Args:
        id (int): The ID of the payment to update.

    Returns:
        Union[Dict[str, str], Tuple[Dict[str, str], int]]: A JSON response containing a success message or an error message, and a status code.

    Raises:
        HTTPException: 401 (Unauthorized) if the payment ID or status is not provided, or the user is not the seller,
                       500 (Internal Server Error) if an error occurs during update.
    """
    try:
        if not id:
            return jsonify({'error': 'Payment ID is required'}), 401
        status = request.form.get('status', None)
        if not status:
            return jsonify({'error': 'Payment status is required'}), 401
        payment = Payment.query.get(id)
        order_id = payment.order_id
        user_id = session.get('user_id')
        order = Order.query.get(order_id)
        if order.seller_id == user_id:
            payment.seller_payment_status = status
            payment.dispatcher_payment_status = status
        else:
            return jsonify({'message': 'You are not the seller'}), 401
        if payment.seller_payment_status == 'paid':
            order.status = 'completed'
        elif payment.seller_payment_status == 'inprocess':
            order.status = 'incomplete'
        else:
            return jsonify({'message': 'Invalid payment status'}), 401      
        
        payment.payment_date_time = datetime.now()
        payment.last_update_time = datetime.now()
        
        db.session.commit()
        return jsonify({'message': 'Payment has been updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An internal error occurred'}), 500


@app_views.route('/payment', methods=['POST'], strict_slashes=False)
@protected_route
def create_payment():
    """
    This endpoint creates a payment.

    Args:
        payment_method (str): The method of payment.
        seller_amount (float): The amount to be paid to the seller.
        dispatcher_amount (float): The amount to be paid to the dispatcher.
        currency (str): The currency of the payment.
        order_id (int): The ID of the order the payment is for.

    Returns:
        Union[Dict[str, str], Tuple[Dict[str, str], int]]: A JSON response containing a success message or an error message, and a status code.

    Raises:
        HTTPException: 401 (Unauthorized) if the user is not the buyer,
                       500 (Internal Server Error) if an error occurs during creation.
    """
    try:
        payment_method = request.form.get('payment_method', None)
        seller_amount = float(request.form.get('seller_amount', None))
        dispatcher_amount = float(request.form.get('dispatcher_amount', None))
        currency = request.form.get('currency', None)
        order_id = int(request.form.get('order_id', None))

        user_id = session.get('user_id')
        order = Order.query.get(order_id)
        if order.buyer_id != user_id:
            return jsonify({'message': 'You are not the buyer'}), 401
            
        payment = Payment(payment_method=payment_method,
                          seller_amount=seller_amount,
                          dispatcher_amount=dispatcher_amount,
                          currency=currency,
                          order_id=order_id
                          )
        order.payment.append(payment)
        db.session.add(payment)
        db.session.commit()
        return jsonify({'message': 'Payment has been created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An internal error occurred'}), 500


@app_views.route('/payments/<int:order_id>', methods=['GET'], strict_slashes=False)
@protected_route
def get_my_payments(order_id=None):
    """
    This endpoint retrieves payments based on the order ID.

    Args:
        order_id (int): The ID of the order to retrieve payments for.

    Returns:
        Union[Dict[str, Union[str, int, float, datetime]], Tuple[Dict[str, str], int]]: A JSON response containing the payment data or an error message, and a status code.

    Raises:
        HTTPException: 401 (Unauthorized) if the order ID is not provided or no payments exist for the order,
                       500 (Internal Server Error) if an error occurs during retrieval.
    """
    try:
        if not order_id:
            return jsonify({'error': 'Order ID is required'}), 401
        user_id = session.get('user_id')
        query = Order.query.filter(
            (Order.seller_id == user_id) |
            (Order.buyer_id == user_id) |
            (Order.dispatcher_id == user_id)
            ).filter_by(id=order_id).one()
        payments = query.payment
        if not payments:
            return jsonify({'message': 'No payment was found'}), 401
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
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An internal error occurred'}), 500

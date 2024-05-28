from flask_server import db
from datetime import datetime
from sqlalchemy import CheckConstraint, text

def validate_payment_method():
    """
    Ensure that the payment method is one of the following: 'transfer', 'cash', 'pos'.
    """
    return "payment_method IN ('transfer', 'cash', 'pos')"

def validate_status():
    """
    Ensure that the payment status is one of the following: 'inprocess', 'unpaid', 'paid'.
    """
    return "seller_payment_status IN ('inprocess', 'unpaid', 'paid')"

def validate_currency():
    """
    Ensure that the currency is one of the following: 'Naira', 'Dollar'.
    """
    return "currency IN ('Naira', 'Dollar')"

class Payment(db.Model):
    """
    This class represents a payment in the database.

    Attributes:
        id (int): The primary key of the payment.
        payment_method (str): The method of payment. It defaults to 'transfer'.
        seller_payment_status (str): The payment status of the seller. It defaults to 'unpaid'.
        dispatcher_payment_status (str): The payment status of the dispatcher. It defaults to 'unpaid'.
        payment_date_time (datetime): The date and time when the payment was made.
        last_update_time (datetime): The date and time when the payment was last updated. It cannot be null and defaults to the current date and time.
        seller_amount (int): The amount paid to the seller. It defaults to 0.
        dispatcher_amount (int): The amount paid to the dispatcher. It defaults to 0.
        order_id (int): The foreign key of the order that the payment is for.
        currency (str): The currency of the payment. It cannot be null and defaults to 'Naira'.
    """
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    payment_method = db.Column(db.String(10), CheckConstraint(text(validate_payment_method())), default='transfer')
    seller_payment_status = db.Column(db.String(10), CheckConstraint(text(validate_status())), default='unpaid')
    dispatcher_payment_status = db.Column(db.String(10), CheckConstraint(text(validate_status())), default='unpaid')	
    payment_date_time = db.Column(db.DateTime, nullable=True)
    last_update_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    seller_amount = db.Column(db.Integer, default=0)
    dispatcher_amount = db.Column(db.Integer, default=0)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=True)
    currency = db.Column(db.String(15), CheckConstraint(text(validate_currency())), nullable=False, default='Naira')
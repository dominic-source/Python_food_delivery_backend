from flask_server import db
from datetime import datetime
from sqlalchemy import CheckConstraint, text


def validate_payment_method():
	"""Ensure that payment method is allowed"""
	return "payment_method IN ('transfer', 'cash', 'pos')"

def validate_status():
	"""Ensure that payment status is correct"""
	return "payment_status IN ('inprocess', 'unpaid', 'paid')"

def validate_currency():
	"""Ensure that currency is accepted"""
	return "currency IN ('Naira', 'Dollar')"


class Payment(db.Model):
	"""This is the users class"""
	__tablename__ = 'payment'
	id = db.Column(db.Integer, primary_key=True)
	payment_method = db.Column(db.String(10), CheckConstraint(text(validate_payment_method())))
	payment_status = db.Column(db.String(10), CheckConstraint(text(validate_status())))
	payment_date_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
	last_update_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
	seller_amount = db.Column(db.Integer, default=0)
	dispatcher_amount = db.Column(db.Integer, default=0)
	total_amount = db.Column(db.Integer, default=0)
	order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=True)
	currency = db.Column(db.String(15), CheckConstraint(text(validate_currency())), nullable=False, default='Naira')

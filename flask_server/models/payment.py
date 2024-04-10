from flask_server import db
from datetime import datetime
from sqlalchemy import CheckConstraint


def validate_payment_method(value):
	"""Ensure that payment method is allowed"""
	method = ['transfer', 'cash', 'pos']
	return value in method

def validate_status(value):
	"""Ensure that payment status is correct"""
	method = ['inprocess', 'unpaid', 'paid']
	return value in method

def validate_currency(value):
	"""Ensure that currency is accepted"""
	currency = ['Naira', 'Dollar']
	return value in currency


class Payment(db.Model):
	"""This is the users class"""
	__tablename__ = 'payment'
	id = db.Column(db.String, primary_key=True)
	payment_method = db.Column(db.String(10), CheckConstraint(validate_payment_method))
	payment_status = db.Column(db.String(10), CheckConstraint(validate_status))
	payment_date_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
	amount = db.Column(db.Integer, default=0)
	currency = db.Column(db.String(15), CheckConstraint(validate_currency), nullable=False, default='Naira')

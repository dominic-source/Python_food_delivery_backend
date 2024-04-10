from flask_server import db
from datetime import datetime
from sqlalchemy import CheckConstraint
from flask_server.models.payment import validate_currency


def validate_status(value):
	"""Ensure that users can only have this types of type"""
	status = ['completed', 'incomplete', 'pending']
	return value in status


class Order(db.Model):
	"""This is the users class"""
	__tablename__ = 'order'
	id = db.Column(db.String, primary_key=True)
	seller_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
	buyer_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
	dispatcher_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
	order_date_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
	currency = db.Column(db.String(15), CheckConstraint(validate_currency), nullable=False, default='Naira')
	delivery_address = db.Column(db.String(120), nullable=False)
	total_amount = db.Column(db.Integer, nullable=False, default=0)
	status = db.Column(db.String, CheckConstraint(validate_status), default='pending')
	payment = db.relationship("Payment", backref='order', uselist=False)
	orderitems = db.relationship('OrderItem', backred='order', cascade='all, delete-orphan')

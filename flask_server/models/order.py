from flask_server import db
from datetime import datetime
from sqlalchemy import CheckConstraint, text
from flask_server.models.payment import validate_currency


def validate_status():
	"""Ensure that users can only have this types of type"""
	return "status IN ('completed', 'incomplete', 'pending')"


class Order(db.Model):
	"""This is the users class"""
	__tablename__ = 'order'
	id = db.Column(db.Integer, primary_key=True)
	seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	dispatcher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	order_date_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
	currency = db.Column(db.String(15), CheckConstraint(text(validate_currency())), nullable=False, default='Naira')
	delivery_address = db.Column(db.String(120), nullable=False)
	total_amount = db.Column(db.Integer, nullable=False, default=0)
	status = db.Column(db.String(15), CheckConstraint(text(validate_status())), default='pending')
	payment = db.relationship("Payment", backref='order', uselist=False)
	orderitems = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan')
	payment_token = db.Column(db.String(120), nullable=True)

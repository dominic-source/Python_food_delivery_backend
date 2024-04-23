from flask_server import db
from datetime import datetime
from sqlalchemy import Enum
import enum

class UserType(enum.Enum):
	"""Ensure that users can only have this types of user type"""
	seller = 'seller'
	dispatcher = 'dispatcher'
	buyer = 'buyer'

class StatusType(enum.Enum):
	"""Ensure that users can only have this types of status"""
	available = 'available'
	busy = 'busy'
	deleted = 'deleted'


class User(db.Model):
	"""This is the users class"""
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(100), nullable=False)
	last_name = db.Column(db.String(100), nullable=False)
	username = db.Column(db.String(30), nullable=False)
	password_hash = db.Column(db.String(120), nullable=False)
	reset_password_token = db.Column(db.String(120), nullable=True)
	email = db.Column(db.String(30), unique=True, nullable=False)
	phone_number = db.Column(db.String(30), nullable=True)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
	updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
	lga_id = db.Column(db.Integer,  db.ForeignKey('lga.id'), nullable=True)
	vehicle_number = db.Column(db.String(30), nullable=True)
	user_type = db.Column(Enum(UserType), nullable=False, default=UserType.buyer)
	status = db.Column(Enum(StatusType), nullable=False, default=StatusType.busy)
	photo = db.Column(db.String(70), nullable=True)
	products = db.relationship('Product', backref='owner', cascade='all, delete-orphan')
	orders_seller = db.relationship('Order', backref='seller',
								 foreign_keys='Order.seller_id', cascade='all, delete-orphan')
	orders_buyer = db.relationship('Order', backref='buyer',
								 foreign_keys='Order.buyer_id', cascade='all, delete-orphan')
	orders_dispatcher = db.relationship('Order', backref='dispatcher',
								 foreign_keys='Order.dispatcher_id', cascade='all, delete-orphan')
	address_seller_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=True)
	address_buyer_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=True)
	address_dispatcher_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=True)


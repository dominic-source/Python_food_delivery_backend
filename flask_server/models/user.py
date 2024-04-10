from flask_server import db
from datetime import datetime
from sqlalchemy import Enum

class UserType(Enum):
	"""Ensure that users can only have this types of user type"""
	seller = 'seller'
	dispatcher = 'dispatcher'
	buyer = 'buyer'

class StatusType(Enum):
	"""Ensure that users can only have this types of status"""
	available = 'available'
	busy = 'busy'


class User(db.Model):
	"""This is the users class"""
	__tablename__ = 'user'
	id = db.Column(db.string, primary_key=True)
	username = db.Column(db.String(30), nullable=False)
	password_hash = db.Column(db.String(120), nullable=False)
	email = db.Column(db.String(30), unique=True, nullable=False)
	phone_number = db.Column(db.String(30), nullable=True)
	address = db.Column(db.String(100), nullable=True)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
	lga_id = db.Column(db.String(120),  db.ForeignKey('lga.id'), nullable=True)
	vehicle_number = db.Column(db.String(30), nullabe=True)
	user_type = db.Column(db.Sting(15), Enum(UserType), nullable=False, default=UserType.buyer)
	status = db.Column(db.String(15), Enum(StatusType), nullable=False, default=StatusType.busy)
	photo = db.Column(db.String(70), nullable=True)
	products = db.relationship('Product', backref='owner', cascade='all, delete-orphan')
	orders_seller = db.relationship('Order', backref='seller',
								 foreign_key='Orders.seller_id', cascade='all, delete-orphan')
	orders_buyer = db.relationship('Order', backref='buyer',
								 foreign_key='Orders.buyer_id', cascade='all, delete-orphan')
	orders_dispatcher = db.relationship('Order', backref='dispatcher',
								 foreign_key='Orders.dispatcher_id', cascade='all, delete-orphan')

from flask_server import db
from datetime import datetime
from sqlalchemy import CheckConstraint
from flask_server.models.payment import validate_currency


class Product(db.Model):
	"""This is the users class"""
	__tablename__ = 'product'
	id = db.Column(db.String, primary_key=True)
	product_name = db.Column(db.String(35), nullable=False)
	description = db.Column(db.String(120), nullable=True)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
	price = db.Column(db.Integer, nullable=False, default=0)
	currency = db.Column(db.String(15), CheckConstraint(validate_currency), nullable=False, default='Naira')
	category_id = db.Column(db.String, db.ForeignKey('category.id'), nullable=False)
	user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
	photo = db.Column(db.String(30), nullable=True)

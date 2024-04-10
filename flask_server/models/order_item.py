from flask_server import db


class OrderItem(db.Model):
	"""This is the users class"""
	__tablename__ = 'orderitem'
	id = db.Column(db.String, primary_key=True)
	order_id = db.Column(db.String, db.ForeignKey('order.id'), nullable=False)
	product_id = db.Column(db.String, db.ForeignKey('product.id'), nullable=False)
	quantity = db.Column(db.Integer, nullable=False, default=0)
	comments = db.Column(db.String(120), nullable=True)
	ratings = db.Column(db.Integer, nullable=True)

from flask_server import db


class Category(db.Model):
	"""This is the users class"""
	__tablename__ = 'category'
	id = db.Column(db.Integer, primary_key=True)
	category_name = db.Column(db.String(35), nullable=False)

from flask_server import db


class Category(db.Model):
	"""This is the users class"""
	__tablename__ = 'category'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(35), unique=True, nullable=False)

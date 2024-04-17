from flask_server import db


class Location(db.Model):
	"""This is the current location of the user"""
	__tablename__ = 'location'
	id = db.Column(db.Integer, primary_key=True)
	address = db.Column(db.String(120), nullable=True)
	lga_id = db.Column(db.Integer, db.ForeignKey('lga.id'), nullable=False)
	longitude = db.Column(db.String(15), nullable=True)
	latitude = db.Column(db.String(15), nullable=True)


class Lga(db.Model):
	"""This is the users lga class"""
	__tablename__ = 'lga'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(35), nullable=False)
	state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)


class State(db.Model):
	"""This is the users state class"""
	__tablename__ = 'state'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(35), nullable=False)
	country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
	lgas = db.relationship('Lga', backref='state', cascade='all, delete-orphan')


class Country(db.Model):
	"""This is the users country class"""
	__tablename__ = 'country'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(35), nullable=False)
	states = db.relationship('State', backref='country', cascade='all, delete-orphan')

from flask_server import db

class Location(db.Model):
    """
    This class represents a user's location in the database.

    Attributes:
        id (int): The primary key of the location.
        address (str): The address of the location.
        lga_id (int): The foreign key of the Local Government Area (LGA) that the location belongs to.
        longitude (str): The longitude of the location.
        latitude (str): The latitude of the location.
    """
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(120), nullable=True)
    lga_id = db.Column(db.Integer, db.ForeignKey('lga.id'), nullable=False)
    longitude = db.Column(db.String(15), nullable=True)
    latitude = db.Column(db.String(15), nullable=True)


class Lga(db.Model):
    """
    This class represents a Local Government Area (LGA) in the database.

    Attributes:
        id (int): The primary key of the LGA.
        name (str): The name of the LGA.
        state_id (int): The foreign key of the state that the LGA belongs to.
    """
    __tablename__ = 'lga'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)


class State(db.Model):
    """
    This class represents a state in the database.

    Attributes:
        id (int): The primary key of the state.
        name (str): The name of the state.
        country_id (int): The foreign key of the country that the state belongs to.
        lgas (List[Lga]): The list of LGAs that belong to the state.
    """
    __tablename__ = 'state'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    lgas = db.relationship('Lga', backref='state', cascade='all, delete-orphan')


class Country(db.Model):
    """
    This class represents a country in the database.

    Attributes:
        id (int): The primary key of the country.
        name (str): The name of the country.
        states (List[State]): The list of states that belong to the country.
    """
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), nullable=False)
    states = db.relationship('State', backref='country', cascade='all, delete-orphan')
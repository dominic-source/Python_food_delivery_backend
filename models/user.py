from flask_server import db
from datetime import datetime
from sqlalchemy import Enum
import enum

class UserType(enum.Enum):
    """
    This enum represents the possible types of users.

    Attributes:
        seller (str): Represents a user who is a seller.
        dispatcher (str): Represents a user who is a dispatcher.
        buyer (str): Represents a user who is a buyer.
    """
    seller = 'seller'
    dispatcher = 'dispatcher'
    buyer = 'buyer'

class StatusType(enum.Enum):
    """
    This enum represents the possible statuses of users.

    Attributes:
        available (str): Represents a user who is available.
        busy (str): Represents a user who is busy.
        deleted (str): Represents a user who is deleted.
    """
    available = 'available'
    busy = 'busy'
    deleted = 'deleted'

class User(db.Model):
    """
    This class represents a user in the database.

    Attributes:
        id (int): The primary key of the user.
        first_name (str): The first name of the user. It cannot be null.
        last_name (str): The last name of the user. It cannot be null.
        username (str): The username of the user. It cannot be null.
        password_hash (str): The hashed password of the user. It cannot be null.
        reset_password_token (str): The reset password token of the user.
        email (str): The email of the user. It cannot be null and must be unique.
        phone_number (str): The phone number of the user.
        created_at (datetime): The date and time when the user was created. It cannot be null and defaults to the current date and time.
        updated_at (datetime): The date and time when the user was last updated. It cannot be null and defaults to the current date and time.
        lga_id (int): The foreign key of the local government area that the user belongs to.
        vehicle_number (str): The vehicle number of the user.
        user_type (UserType): The type of the user. It cannot be null and defaults to UserType.buyer.
        status (StatusType): The status of the user. It cannot be null and defaults to StatusType.available.
        photo (str): The photo of the user.
        products (list of Product): The products that the user owns.
        orders_seller (list of Order): The orders that the user has as a seller.
        orders_buyer (list of Order): The orders that the user has as a buyer.
        orders_dispatcher (list of Order): The orders that the user has as a dispatcher.
        address_seller_id (int): The foreign key of the location of the seller.
        address_buyer_id (int): The foreign key of the location of the buyer.
        address_dispatcher_id (int): The foreign key of the location of the dispatcher.
    """
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
    status = db.Column(Enum(StatusType), nullable=False, default=StatusType.available)
    photo = db.Column(db.String(70), nullable=True)
    products = db.relationship('Product', backref='owner',
                            foreign_keys='Product.user_id', cascade='all, delete-orphan')
    orders_seller = db.relationship('Order', backref='seller',
                                 foreign_keys='Order.seller_id', cascade='all, delete-orphan')
    orders_buyer = db.relationship('Order', backref='buyer',
                                 foreign_keys='Order.buyer_id', cascade='all, delete-orphan')
    orders_dispatcher = db.relationship('Order', backref='dispatcher',
                                 foreign_keys='Order.dispatcher_id', cascade='all, delete-orphan')
    address_seller_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=True)
    address_buyer_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=True)
    address_dispatcher_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=True)
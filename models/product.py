from flask_server import db
from datetime import datetime
from sqlalchemy import CheckConstraint, text
from flask_server.models.payment import validate_currency

class Product(db.Model):
    """
    This class represents a product in the database.

    Attributes:
        id (int): The primary key of the product.
        name (str): The name of the product. It cannot be null.
        description (str): The description of the product.
        created_at (datetime): The date and time when the product was created. It cannot be null and defaults to the current date and time.
        updated_at (datetime): The date and time when the product was last updated. It cannot be null and defaults to the current date and time.
        price (int): The price of the product. It cannot be null and defaults to 0.
        currency (str): The currency of the product. It cannot be null and defaults to 'Naira'.
        category_id (int): The foreign key of the category that the product belongs to. It cannot be null.
        user_id (int): The foreign key of the user who created the product. It cannot be null.
        photo (str): The photo of the product.
        quantity (int): The quantity of the product. It cannot be null and defaults to 0.
    """
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), nullable=False)
    description = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    price = db.Column(db.Integer, nullable=False, default=0)
    currency = db.Column(db.String(15), CheckConstraint(text(validate_currency())), nullable=False, default='Naira')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    photo = db.Column(db.String(30), nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
from flask_server import db

class OrderItem(db.Model):
    """
    This class represents an item in an order in the database.

    Attributes:
        id (int): The primary key of the order item.
        order_id (int): The foreign key of the order that the item belongs to.
        product_id (int): The foreign key of the product that the item is.
        quantity (int): The quantity of the product in the order. It cannot be null and defaults to 0.
        comments (str): Any comments on the order item.
        ratings (int): The rating of the order item.
    """
    __tablename__ = 'orderitem'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    comments = db.Column(db.String(120), nullable=True)
    ratings = db.Column(db.Integer, nullable=True)
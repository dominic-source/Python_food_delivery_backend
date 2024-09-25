from flask_server import db
from datetime import datetime
from sqlalchemy import CheckConstraint, text
from flask_server.models.payment import validate_currency

def validate_status():
    """
    Ensure that the status of an order can only be one of the following: 'completed', 'incomplete', 'pending'.
    """
    return "status IN ('completed', 'incomplete', 'pending')"

class Order(db.Model):
    """
    This class represents an order in the database.

    Attributes:
        id (int): The primary key of the order.
        seller_id (int): The foreign key of the user who is the seller.
        buyer_id (int): The foreign key of the user who is the buyer.
        dispatcher_id (int): The foreign key of the user who is the dispatcher.
        order_date_time (datetime): The date and time when the order was placed. It cannot be null and defaults to the current date and time.
        currency (str): The currency of the order. It cannot be null and defaults to 'Naira'.
        delivery_address (str): The delivery address for the order. It cannot be null.
        total_amount (int): The total amount of the order. It cannot be null and defaults to 0.
        status (str): The status of the order. It defaults to 'pending'.
        payment (Payment): The payment for the order.
        orderitems (List[OrderItem]): The items in the order.
    """
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dispatcher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_date_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    currency = db.Column(db.String(15), CheckConstraint(text(validate_currency())), nullable=False, default='Naira')
    delivery_address = db.Column(db.String(120), nullable=False)
    total_amount = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(15), CheckConstraint(text(validate_status())), default='pending')
    payment = db.relationship("Payment", backref='order', cascade='all, delete-orphan')
    orderitems = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan')
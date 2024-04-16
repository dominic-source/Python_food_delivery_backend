""" This module is used to login in user for authentication purposes
"""
from flask_server.views.v1 import app_views
from flask import request, jsonify, make_response, session
from flask_server.models import User
from flask_server import db

@app_views.route('/', strict_slashes=False, methods=['GET', 'POST'])
def user():
    """Test the user"""
    user = User(username="chinonso", password_hash="fasofij", email="chinonsodomnic@gmail.com")
    user.orders_buyer=[]
    user.orders_dispatcher=[]
    user.orders_seller=[]
    db.session.add(user)
    db.session.commit()
    return jsonify(user)

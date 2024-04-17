""" This module is used to login in user for authentication purposes
"""
from flask_server.views.v1 import app_views
from flask import request, jsonify, make_response, session
from flask_server.models import User
from flask_server import db

@app_views.route('/', strict_slashes=False, methods=['GET', 'POST'])
def user():
    """Test the user"""
    user = User(username="Loveth", password_hash="fasofij", email="Loveth@gmail.com")
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username, 'date': user.created_at})

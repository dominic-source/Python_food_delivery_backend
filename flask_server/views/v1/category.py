""" This module is used to login in user for authentication purposes
"""
from flask_server.views.v1 import app_views, protected_route, logger
from flask import request, jsonify, make_response, session
from flask_server.models import Category
from flask_server import db


@app_views.route('category', methods=['POST'], strict_slashes=False)
@protected_route
def create_category():
    """This endpoint creates a category"""
    try:
        category_name = request.form.get('name', None)
        if not category_name:
            return ({'error': 'Category name must be indicated'})
        category = Category(category_name=category_name)
        db.session.add(category)
        db.session.commit()
        return jsonify({'success': category.category_name + ' ' + category.id}), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occured:", exc_info=True)
        return jsonify({'error': 'An error occured!'}), 401


@app_views.route('/categories', methods=['GET'], strict_slashes=False)
@protected_route
def all_categories():
    """This endpoint retrieves all categories"""
    try:
        if id is None:
            return jsonify({'error': 'An error occured!'}), 401
        category = db.session.query(Category).all()
        if not category:
            return jsonify({'success': 'No category was found'}), 401
        return jsonify(category), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occured:", exc_info=True)
        return jsonify({'error': 'An error occured!'}), 401


@app_views.route('/category/<id>', methods=['GET'], strict_slashes=False)
@protected_route
def get_category(id=None):
    """This endpoint is meant to retrieve a particular category by its ID"""
    try:
        if id is None:
            return jsonify({'error': 'An error occured!'}), 401
        category = db.session.query(Category).filter_by(id=id).one()
        if not category:
            return jsonify({'success': 'The category was not found'}), 401
        return jsonify(category), 200

    except Exception as e:
        db.session.rollback()
        logger.error("Error occured:", exc_info=True)
        return jsonify({'error': 'An error occured!'}), 401

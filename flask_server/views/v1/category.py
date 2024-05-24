""" This module is used for to manage the categories
"""
from flask_server.views.v1 import admin_route, app_views, protected_route, logger
from flask import request, jsonify, make_response, session
from flask_server.models import Category
from flask_server import db


@app_views.route('/category/<id>', methods=['DELETE'], strict_slashes=False)
@admin_route
@protected_route
def delete_category(id=None):
    """This endpoint will delete a category"""
    try:
        if not id:
            return jsonify({'error': 'Category Id is required!'}), 401
        category = db.session.query(Category).filter_by(id=id).first()
        if not category:
            return jsonify({'error': 'An error occured!'}), 401
        db.session.delete(category)
        db.session.commit()
        return jsonify({'success': 'Successfully delete the category!'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occured:", exc_info=True)
        return jsonify({'error': 'An error occured!'}), 401


@app_views.route('/category', methods=['POST'], strict_slashes=False)
@admin_route
@protected_route
def create_category():
    """This endpoint creates a category"""
    try:
        name = request.form.get('name', None)
        if not name:
            return ({'error': 'Category name must be indicated'})
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return jsonify({'name': category.name, 'id': category.id}), 200
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
        categories = db.session.query(Category).all()
        if not categories:
            return jsonify({'success': 'No category was found'}), 401
        category_data = [{'id':category.id, 'name': category.name} for category in categories]
        return jsonify(category_data), 200
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
        category_data = {'name': category.name, 'id': category.id}
        return jsonify(category_data), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occured:", exc_info=True)
        print(e)
        return jsonify({'error': 'An error occured!'}), 401

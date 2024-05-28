""" 
This module is used to manage the categories
"""
from flask_server.views.v1 import admin_route, app_views, protected_route, logger
from flask import request, jsonify
from flask_server.models import Category
from flask_server import db
from typing import Any, Dict, List, Union, Tuple


@app_views.route('/category/<int:id>', methods=['DELETE'], strict_slashes=False)
@admin_route
@protected_route
def delete_category(id: int) -> Union[Dict[str, str], Tuple[Dict[str, str], int]]:
    """This endpoint will delete a category"""
    if not id:
        return jsonify({'error': 'Category ID is required!'}), 400
    try:
        category = db.session.query(Category).filter_by(id=id).first()
        if not category:
            return jsonify({'error': 'Category not found!'}), 404
        db.session.delete(category)
        db.session.commit()
        return jsonify({'success': 'Category deleted successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An error occurred!'}), 500


@app_views.route('/category', methods=['POST'], strict_slashes=False)
@admin_route
@protected_route
def create_category() -> Union[Dict[str, Union[str, int]], Tuple[Dict[str, str], int]]:
    """This endpoint creates a category"""
    name: str = request.form.get('name', None)
    if not name:
        return jsonify({'error': 'Category name must be provided!'}), 400
    try:
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return jsonify({'name': category.name, 'id': category.id}), 201
    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An error occurred!'}), 500


@app_views.route('/categories', methods=['GET'], strict_slashes=False)
@protected_route
def all_categories() -> Union[Dict[str, Union[str, int]], Tuple[Dict[str, str], int]]:
    """This endpoint retrieves all categories"""
    try:
        categories: List[Category] = db.session.query(Category).all()
        if not categories:
            return jsonify({'error': 'No categories found!'}), 404
        category_data: List[Dict[str, Union[str, int]]] = [{'id': category.id, 'name': category.name} for category in categories]
        return jsonify(category_data), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An error occurred!'}), 500


@app_views.route('/category/<int:id>', methods=['GET'], strict_slashes=False)
@protected_route
def get_category(id: int) -> Union[Dict[str, Union[str, int]], Tuple[Dict[str, str], int]]:
    """This endpoint retrieves a particular category by its ID"""
    if not id:
        return jsonify({'error': 'Category ID is required!'}), 400
    try:
        category: Category = db.session.query(Category).filter_by(id=id).one()
        if not category:
            return jsonify({'error': 'Category not found!'}), 404
        category_data: Dict[str, Union[str, int]] = {'name': category.name, 'id': category.id}
        return jsonify(category_data), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An error occurred!'}), 500

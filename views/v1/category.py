""" 
This module is used to manage the categories
"""
from flask_server.views.v1 import admin_route, app_views, protected_route, logger
from flask import request, jsonify
from flask_server.models import Category
from flask_server import db
from typing import Dict, List, Union, Tuple


@app_views.route('/category/<int:id>', methods=['DELETE'], strict_slashes=False)
@admin_route
@protected_route
def delete_category(id: int) -> Union[Dict[str, str], Tuple[Dict[str, str], int]]:
    """
    This endpoint deletes a category.

    Args:
        id (int): The ID of the category to delete.

    Returns:
        Union[Dict[str, str], Tuple[Dict[str, str], int]]: A JSON response containing a success message or an error message, and a status code.

    Raises:
        HTTPException: 400 (Bad Request) if the category ID is not provided,
                       404 (Not Found) if the category does not exist,
                       500 (Internal Server Error) if an error occurs during deletion.
    """
    if not id:
        return jsonify({'error': 'Category ID is required'}), 400
    try:
        category = Category.query.get(id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An internal error occurred'}), 500


@app_views.route('/category', methods=['POST'], strict_slashes=False)
@admin_route
@protected_route
def create_category() -> Union[Dict[str, Union[str, int]], Tuple[Dict[str, str], int]]:
    """
    This endpoint creates a category.

    Args:
        name (str): The name of the category to create.

    Returns:
        Union[Dict[str, Union[str, int]], Tuple[Dict[str, str], int]]: A JSON response containing the name and ID of the created category, or an error message, and a status code.

    Raises:
        HTTPException: 400 (Bad Request) if the category name is not provided,
                       500 (Internal Server Error) if an error occurs during creation.
    """
    name: str = request.form.get('name', None)
    if not name:
        return jsonify({'error': 'Category name must be provided'}), 400
    try:
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return jsonify({'name': category.name, 'id': category.id}), 201
    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An internal error occurred'}), 500


@app_views.route('/categories', methods=['GET'], strict_slashes=False)
@protected_route
def all_categories() -> Union[Dict[str, Union[str, int]], Tuple[Dict[str, str], int]]:
    """
    This endpoint retrieves all categories.

    Returns:
        Union[Dict[str, Union[str, int]], Tuple[Dict[str, str], int]]: A JSON response containing a list of categories or an error message, and a status code.

    Raises:
        HTTPException: 404 (Not Found) if no categories exist,
                       500 (Internal Server Error) if an error occurs during retrieval.
    """
    try:
        categories: List[Category] = Category.query.all()
        if not categories:
            return jsonify({'error': 'No categories found'}), 404
        category_data: List[Dict[str, Union[str, int]]] = [{'id': category.id, 'name': category.name} for category in categories]
        return jsonify(category_data), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An internal error occurred'}), 500


@app_views.route('/category/<int:id>', methods=['GET'], strict_slashes=False)
@protected_route
def get_category(id: int) -> Union[Dict[str, Union[str, int]], Tuple[Dict[str, str], int]]:
    """
    This endpoint retrieves a particular category by its ID.

    Args:
        id (int): The ID of the category to retrieve.

    Returns:
        Union[Dict[str, Union[str, int]], Tuple[Dict[str, str], int]]: A JSON response containing the category data or an error message, and a status code.

    Raises:
        HTTPException: 400 (Bad Request) if the category ID is not provided,
                       404 (Not Found) if the category does not exist,
                       500 (Internal Server Error) if an error occurs during retrieval.
    """
    if not id:
        return jsonify({'error': 'Category ID is required'}), 400
    try:
        category: Category = Category.query.get(id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        category_data: Dict[str, Union[str, int]] = {'name': category.name, 'id': category.id}
        return jsonify(category_data), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An internal error occurred'}), 500

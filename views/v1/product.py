""" This module is used to manage the product
"""
from flask_server.views.v1 import app_views, protected_route, logger
from flask import request, jsonify, make_response, session
from flask_server.models import Product, Category, User
from flask_server import db
from datetime import datetime


@app_views.route('/products/categories/<int:id>', methods=['GET'], strict_slashes=False)
@protected_route
def categories_products(id=None):
    """
    This endpoint retrieves all unique product names in a specific category.

    Args:
        id (int): The ID of the category.

    Returns:
        Union[Dict[str, str], Tuple[Dict[str, str], int]]: A JSON response containing the product names or an error message, and a status code.

    Raises:
        HTTPException: 400 (Bad Request) if the category ID is not provided,
                       404 (Not Found) if no products exist in the category,
                       500 (Internal Server Error) if an internal error occurs.
    """
    try:
        if id is None:
            return jsonify({'error': 'Category ID is required'}), 400
        products = db.session.query(Product.name).filter(Product.category_id == id).distinct().all()
        if not products:
            return jsonify({'error': 'No products found in this category'}), 404
        product_data = [{'name': product.name} for product in products]
        return jsonify(product_data), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An internal error occurred'}), 500


@app_views.route('/products/users', methods=['GET'], strict_slashes=False)
@protected_route
def users_products():
    """
    This endpoint retrieves all products associated with the current user.

    Returns:
        Union[Dict[str, str], Tuple[Dict[str, str], int]]: A JSON response containing the product data or an error message, and a status code.

    Raises:
        HTTPException: 404 (Not Found) if the user does not exist or has no products,
                       500 (Internal Server Error) if an internal error occurs.
    """
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not logged in'}), 401
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        product_data = [{'id': product.id, 'name': product.name, 'quantity': product.quantity, 'price': product.price} for product in user.products]
        if not product_data:
            return jsonify({'error': 'No products found for user'}), 404
        return jsonify(product_data), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An internal error occurred'}), 500


@app_views.route('/product/<int:id>', methods=['PUT'], strict_slashes=False)
@protected_route
def update_products(id=None):
    """
    This endpoint updates a product by its ID.

    Args:
        id (int): The ID of the product to update.

    Returns:
        Union[Dict[str, str], Tuple[Dict[str, str], int]]: A JSON response containing the updated product data or an error message, and a status code.

    Raises:
        HTTPException: 400 (Bad Request) if the product ID is not provided,
                       404 (Not Found) if the product does not exist,
                       500 (Internal Server Error) if an internal error occurs.
    """
    try:
        if id is None:
            return jsonify({'error': 'Product ID is required'}), 400
        product = Product.query.get(id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        data = {
            'name': request.form.get('name'),
            'description': request.form.get('description'),
            'price': float(request.form.get('price')) if request.form.get('price') else None,
            'currency': request.form.get('currency'),
            'category_id': int(request.form.get('category_id')) if request.form.get('category_id') else None,
            'quantity': int(request.form.get('quantity')) if request.form.get('quantity') else None
        }
        for k, v in data.items():
            if v is not None:
                setattr(product, k, v)
        product.updated_at = datetime.now()
        product_data = {
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'price': product.price,
            'updated_at': product.updated_at,
            'created_at': product.created_at,
            'currency': product.currency
        }
        db.session.commit()
        return jsonify(product_data), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An internal error occurred'}), 500


@app_views.route('/products', methods=['GET'], strict_slashes=False)
@protected_route
def all_products():
    """
    This endpoint retrieves all products.

    Returns:
        Union[Dict[str, str], Tuple[Dict[str, str], int]]: A JSON response containing the product data or an error message, and a status code.

    Raises:
        HTTPException: 404 (Not Found) if no products exist,
                       500 (Internal Server Error) if an internal error occurs.
    """
    try:
        products = Product.query.all()
        if not products:
            return jsonify({'error': 'No products found'}), 404
        product_data = [{'id': product.id, 'name': product.name, 'quantity': product.quantity, 'price': product.price} for product in products]
        return jsonify(product_data), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An internal error occurred'}), 500


@app_views.route('/product/<int:id>', methods=['GET'], strict_slashes=False)
@protected_route
def get_product(id=None):
    """
    This endpoint retrieves a product by its ID.

    Args:
        id (int): The ID of the product to retrieve.

    Returns:
        Union[Dict[str, str], Tuple[Dict[str, str], int]]: A JSON response containing the product data or an error message, and a status code.

    Raises:
        HTTPException: 400 (Bad Request) if the product ID is not provided,
                       404 (Not Found) if the product does not exist,
                       500 (Internal Server Error) if an internal error occurs.
    """
    try:
        if id is None:
            return jsonify({'error': 'Product ID is required'}), 400
        product = Product.query.get(id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        product_data = {
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'price': product.price
        }
        return jsonify(product_data), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An internal error occurred'}), 500


@app_views.route('/product', methods=['POST'], strict_slashes=False)
@protected_route
def create_product():
    """
    This endpoint creates a product.

    Args:
        name (str): The name of the product.
        description (str): The description of the product.
        price (float): The price of the product.
        currency (str): The currency of the product.
        category_id (int): The ID of the category the product belongs to.
        quantity (int): The quantity of the product.

    Returns:
        Union[Dict[str, str], Tuple[Dict[str, str], int]]: A JSON response containing the product ID, name, and owner's username, or an error message, and a status code.

    Raises:
        HTTPException: 401 (Unauthorized) if an error occurs during creation,
                       500 (Internal Server Error) if an internal error occurs.
    """
    try:
        name = request.form.get('name', None)
        description = request.form.get('description', None)
        price = float(request.form.get('price', None))
        currency = request.form.get('currency', None)
        category_id = int(request.form.get('category_id', None))
        quantity = int(request.form.get('quantity', None))

        category = Category.query.get(category_id)
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        product = Product(name=name,
                          description=description,
                          price=price,
                          currency=currency, 
                          category_id=category.id,
                          quantity=quantity,
                          user_id=user_id)
        product.owner = user
        db.session.add(product)
        db.session.commit()
        return jsonify({'id': product.id, 'name': product.name, 'username': product.owner.username}), 201
    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An internal error occurred'}), 500


@app_views.route('/product/<int:id>', methods=['DELETE'], strict_slashes=False)
@protected_route
def delete_product(id=None):
    """
    This endpoint deletes a product.

    Args:
        id (int): The ID of the product to delete.

    Returns:
        Union[Dict[str, str], Tuple[Dict[str, str], int]]: A JSON response containing a success message or an error message, and a status code.

    Raises:
        HTTPException: 401 (Unauthorized) if the product ID is not provided or the product does not exist,
                       500 (Internal Server Error) if an error occurs during deletion.
    """
    try:
        if not id:
            return jsonify({'error': 'Product ID is required'}), 401
        product = Product.query.get(id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        db.session.delete(product)
        db.session.commit()
        return jsonify({'success': 'Product deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An internal error occurred'}), 500

""" This module is used to manage the product
"""
from flask_server.views.v1 import app_views, protected_route, logger
from flask import request, jsonify, make_response, session
from flask_server.models import Product, Category, User
from flask_server import db
from datetime import datetime


@app_views.route('/products/categories/<id>', methods=['GET'], strict_slashes=False)
@protected_route
def categories_products(id=None):
    """This endpoint retrieves all usersproducts"""
    try:
        if id is None:
            return jsonify({'error': 'An error occured!'}), 401
        # To avoid duplicates
        products = db.session.query(Product.name).distinct().filter_by(category_id=id).all()
        product_data = [{'name': product.name} for product in products]
        return jsonify(product_data), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        logger.error("Error occured:", exc_info=True)
        return jsonify({'error': 'An error occured!'}), 401


@app_views.route('/products/users', methods=['GET'], strict_slashes=False)
@protected_route
def users_products():
    """This endpoint retrieves all usersproducts"""
    try:
        user = db.session.query(User).filter_by(id=session.get('user_id')).one()
        product_data = [{'id':product.id, 'name': product.name, 'quantity': product.quantity, 'price': product.price} for product in user.products]
        return jsonify(product_data), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occured:", exc_info=True)
        return jsonify({'error': 'An error occured!'}), 401


@app_views.route('/product/<id>', methods=['PUT'], strict_slashes=False)
@protected_route
def update_products(id=None):
    """This endpoint updates products"""
    try:
        if id is None:
            return jsonify({'error': 'An error occured!'}), 401
        product = db.session.query(Product).filter_by(id=id).one()
        data = {
            'name': request.form.get('name', None),
            'description': request.form.get('description', None),
            'price': request.form.get('price', None),
            'currency': request.form.get('currency', None),
            'category_id': request.form.get('category_id', None),
            'quantity': request.form.get('quantity', None)
        }
        for k, v in data.items():
            if v:
                setattr(product, k, v)
        setattr(product, 'updated_at', datetime.now())
        product_data = {
            'id':product.id,
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
        logger.error("Error occured:", exc_info=True)
        return jsonify({'error': 'An error occured!'}), 401


@app_views.route('/products', methods=['GET'], strict_slashes=False)
@protected_route
def all_products():
    """This endpoint retrieves all products"""
    try:
        products = db.session.query(Product).all()
        if not products:
            return jsonify({'success': 'No product was found'}), 401
        product_data = [{'id':product.id, 'name': product.name, 'quantity': product.quantity, 'price': product.price} for product in products]
        return jsonify(product_data), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occured:", exc_info=True)
        return jsonify({'error': 'An error occured!'}), 401


@app_views.route('/product/<id>', methods=['GET'], strict_slashes=False)
@protected_route
def get_product(id=None):
    """This endpoint is meant to retrieve a particular category by its ID"""
    try:
        if id is None:
            return jsonify({'error': 'An error occured!'}), 401
        product = db.session.query(Product).filter_by(id=id).one()
        if not product:
            return jsonify({'success': 'The product was not found'}), 401
        product_data = {
            'id':product.id,
            'name': product.name,
            'quantity': product.quantity,
            'price': product.price}
        return jsonify(product_data), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occured:", exc_info=True)
        return jsonify({'error': 'An error occured!'}), 401


@app_views.route('/product', methods=['POST'], strict_slashes=False)
@protected_route
def create_product():
    """This endpoint will delete a category"""
    try:
        name = request.form.get('name', None)
        description = request.form.get('description', None)
        price = request.form.get('price', None)
        currency = request.form.get('currency', None)
        category_id = request.form.get('category_id', None)
        quantity = request.form.get('quantity', None)

        category = Category.query.filter_by(id=category_id).one()
        product = Product(name=name,
                         description=description,
                         price=price,
                         currency=currency, 
                         category_id=category.id,
                         quantity=quantity,
                         user_id=session.get('user_id'))
        user = User.query.filter_by(id=session.get('user_id')).one()
        product.owner = user
        db.session.add(product)
        db.session.commit()
        return jsonify({'id': product.id, 'name': product.name, 'username': product.owner.username}), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        logger.error("Error occured:", exc_info=True)
        return jsonify({'error': 'An error occured!'}), 401


@app_views.route('/product/<id>', methods=['DELETE'], strict_slashes=False)
@protected_route
def delete_product(id=None):
    """This endpoint will delete a category"""
    try:
        if not id:
            return jsonify({'error': 'An error occured!'}), 401
        product = db.session.query(Product).filter_by(id=id).first()
        if not product:
            return jsonify({'error': 'An error occured!'}), 401
        db.session.delete(product)
        db.session.commit()
        return jsonify({'success': 'Successfully delete a product!'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occured:", exc_info=True)
        return jsonify({'error': 'An error occured!'}), 401

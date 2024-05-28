""" This module is used to login in user for authentication purposes
"""
from flask_server.views.v1 import admin_route, app_views, protected_route, logger
from flask import request, jsonify, session
from flask_server.models import User, Lga
from flask_server import allowed_file, db, UPLOAD_FOLDER, bcrypt
from flask_server.auth import auth
from werkzeug.utils import secure_filename
import os


@app_views.route('/user', methods=['GET'], strict_slashes=False)
@protected_route
def get_user():
    """
    Retrieve the basic information of a user.

    Returns:
        Union[Dict[str, str], Tuple[Dict[str, str], int]]: A JSON response containing the user's information and status code if the retrieval is successful, or an error message and status code if the retrieval fails.

    Raises:
        HTTPException: 200 (OK) if the retrieval is successful,
                       400 (Bad Request) if the retrieval fails.
    """
    try:
        user = User.query.get(session.get('user_id'))
        if user is None:
            return jsonify({'error': 'User not found'}), 404

        user_data = {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone_number': user.phone_number,
                'vehicle_number': user.vehicle_number,
                'user_type': user.user_type.value,
                'photo': user.photo,
                'status': user.status.value,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            }
        return jsonify(user_data), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': 'An error occurred!'}), 400


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@admin_route
@protected_route
def get_users():
    """
    Retrieve all users of the software.

    Returns:
        Union[List[Dict[str, str]], Tuple[List[Dict[str, str]], int]]: A JSON response containing a list of users and status code if the retrieval is successful, or an error message and status code if the retrieval fails.

    Raises:
        HTTPException: 200 (OK) if the retrieval is successful,
                       400 (Bad Request) if the retrieval fails.
    """
    try:
        users = User.query.all()
        users_data = [{
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            } for user in users]
        return jsonify(users_data), 200
    except Exception as e:
        logger.error("Error occurred:", exc_info=True)
        db.session.rollback()
        return jsonify({'error': 'An error occurred!'}), 400


@app_views.route('/update_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """
    Update a user's password.

    Returns:
        Union[Dict[str, str], Tuple[Dict[str, str], int]]: A JSON response containing a success message and status code if the password update is successful, or an error message and status code if the password update fails.

    Raises:
        HTTPException: 200 (OK) if the password update is successful,
                       400 (Bad Request) if the password update fails.
    """
    if auth.update_password():
        return jsonify({'message': 'Password updated successfully'}), 200
    else:
        return jsonify({'error': 'An error occurred!'}), 400


@app_views.route('/forgot_password', methods=['POST'], strict_slashes=False)
def forgot_password():
    """
    Generate a token for a user who forgot their password.

    Returns:
        Union[Dict[str, str], Tuple[Dict[str, str], int]]: A JSON response containing a success message and status code if the token is generated successfully, or an error message and status code if the token generation fails.

    Raises:
        HTTPException: 200 (OK) if the token is generated successfully,
                       400 (Bad Request) if the token generation fails.
    """
    token = auth.forgot_password()
    if token:
        return jsonify({"message": "A token was sent to your email!"}), 200
    else:
        return jsonify({"error": "An error occurred!"}), 400


@app_views.route('/update_user', methods=['PUT'], strict_slashes=False)
@protected_route
def update_user():
    """
    Update a user's information.

    Returns:
        Union[Dict[str, str], Tuple[Dict[str, str], int]]: A JSON response containing a success message and status code if the update is successful, or an error message and status code if the update fails.

    Raises:
        HTTPException: 200 (OK) if the update is successful,
                       400 (Bad Request) if the update fails.
    """
    try:
        obj = {
            "first_name": request.form.get("first_name", None),
            "last_name": request.form.get("last_name", None),
            "username": request.form.get("username", None),
            "email": request.form.get("email"),
            "vehicle_number": request.form.get("vehicle_number"),
            "user_type": request.form.get("user_type", None),
            "lga_id": request.form.get("lga_id", None),
            "phone_number": request.form.get("phone_number", None),
            "status": request.form.get("status", None)
        }
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        if user is None:
            return jsonify({'error': 'User not found'}), 404

        for key, val in obj.items():
            if val:
                setattr(user, key, val)
        db.session.commit()
        return jsonify({'message': 'User profile updated successfully'}), 200
    except Exception as e:
        logger.error("Error occurred:", exc_info=True)
        db.session.rollback()
        return jsonify({'error': 'An error occurred!'}), 400


@app_views.route('/logout', methods=['POST'], strict_slashes=False)
@protected_route
def logout_user():
    """
    Log out a user.

    Returns:
        Union[str, Tuple[str, int]]: A success message and status code if the logout is successful, or an error message and status code if the logout fails.

    Raises:
        HTTPException: 200 (OK) if the logout is successful,
                       401 (Unauthorized) if the logout fails.
    """
    if auth.logout_user():
        return jsonify({'message': 'User logout successful'}), 200
    else:
        return jsonify({'error': 'Unauthorized user'}), 401


@app_views.route('/login', methods=['POST'], strict_slashes=False)
def login_user():
    """
    Log in a user.

    Returns:
        Union[str, Tuple[str, int]]: A success message and status code if the login is successful, or an error message and status code if the login fails.

    Raises:
        HTTPException: 200 (OK) if the login is successful,
                       401 (Unauthorized) if the login fails.
    """
    if auth.login_user():
        return jsonify({'message': 'User log in successful'}), 200
    else:
        return jsonify({'error': 'Email or password incorrect'}), 401


@app_views.route('/register', strict_slashes=False, methods=['POST'])
def register():
    """
    Register a new user.

    Returns:
        Union[Dict[str, str], Tuple[Dict[str, str], int]]: A JSON response containing the new user's username, creation date, and ID, or an error message, and a status code.

    Raises:
        HTTPException: 400 (Bad Request) if required fields are missing or if the email or phone number is already in use,
                       201 (Created) if the user is successfully created,
                       500 (Internal Server Error) if an internal error occurs.
    """
    required_fields = ['first_name', 'last_name', 'username', 'password', 'email', 'phone_number']
    for field in required_fields:
        if not request.form.get(field):
            return jsonify({'error': f'{field} is required'}), 400

    first_name = request.form.get('first_name')
    if not first_name:
        return jsonify({'data': 'first_name required!'}), 400
    last_name = request.form.get('last_name')
    if not last_name:
        return jsonify({'data': 'last_name required!'}), 400
    username = request.form.get('username')
    if not username:
        return jsonify({'data': 'username required!'}), 400
    password = request.form.get('password')
    if not password:
        return jsonify({'data': 'password required!'}), 400
    email = request.form.get('email')
    if not email:
        return jsonify({'data': 'email required!'}), 400
    phone_number = request.form.get('phone_number')
    if not phone_number:
        return jsonify({'data': 'phone_number required!'}), 400

    lga_id = request.form.get('lga_id')
    vehicle_number = request.form.get('vehicle_number')
    user_type = request.form.get('user_type')
    status = request.form.get('status')

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email is already in use'}), 400
    if User.query.filter_by(phone_number=phone_number).first():
        return jsonify({'error': 'Phone number is already in use'}), 400

    photo = None
    if 'file' in request.files:
        file = request.files['file']
        if file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            photo = filename

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    if lga_id and not Lga.query.get(lga_id):
        lga_id = None

    try:
        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            vehicle_number=vehicle_number,
            user_type=user_type,
            lga_id=lga_id,
            photo=photo,
            phone_number=phone_number,
            status=status,
            password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return jsonify({'username': user.username, 'date': user.created_at, 'id': user.id}), 201
    except Exception as e:
        db.session.rollback()
        logger.error("Error occurred:", exc_info=True)
        return jsonify({'error': str(e)}), 500

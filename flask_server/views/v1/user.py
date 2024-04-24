""" This module is used to login in user for authentication purposes
"""
from flask_server.views.v1 import app_views
from flask import request, jsonify, make_response, session
from flask_server.models import User, Lga
from flask_server import allowed_file, db, app, bcrypt
from werkzeug.utils import secure_filename
import os

@app_views.route('/register', strict_slashes=False, methods=['POST'])
def register():
    """register a user"""
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
    photo = None
    # store images in static folder
    if 'file' in request.files:
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                photo = filename
    user_check_email = db.session.query(User).filter_by(email=email).all()
    if user_check_email:
        return jsonify({'data': 'user already registered!'})
    user_check_number = db.session.query(User).filter_by(phone_number=phone_number).all()
    if user_check_number:
        return jsonify({'data': 'Phone number is taken!'})
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    if lga_id:
        lga = db.session.query(Lga).filter_by(id=lga_id).all()
        if not lga:
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
        return jsonify({'username': user.username, 'date': user.created_at, 'id': user.id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 401
    # return jsonify({'username': user.username, 'date': user.created_at, 'id': user.id}), 200

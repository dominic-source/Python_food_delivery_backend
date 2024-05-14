import unittest
from flask_testing import TestCase
from flask import Flask
from .. import db
from ..views.v1 import app_views
import io

class TestUser(TestCase):
    """This class is meant to test case that has to do with the user"""

    def create_app(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.register_blueprint(app_views)
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
        return self.app

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_signup_v1(self):
        with self.client:
            with open("/home/dominic-source/Pictures/Screenshots/dash.png", 'rb') as file:
                buffer = io.BytesIO(file.read())
            buffer.seek(0)
            file = buffer, 'picture1.png'
            data2 = {
            'first_name': 'Loveth',
            'last_name': 'Ubah',
            'username': 'sdominic',
            'vehicle_number': 'sRaymond',
            'email': 'aymond@gmail.com',
            'password': '112345',
            'phone_number': '233455632',
            'status': 'busy',
            'file': file
            }
            headers = {'Content-Type': 'multipart/form-data'}
            response = self.client.post('/api/register', data=data2, headers=headers)
        data = response.json
        self.assertEqual(response.status_code, 201)
        self.assertTrue('username' in data)
    
    def test_signup_v2(self):
        with self.client:
            with open("/home/dominic-source/Pictures/Screenshots/dash.png", 'rb') as file:
                buffer = io.BytesIO(file.read())
            buffer.seek(0)
            file = buffer, 'picture1.png'
            data2 = {
            'first_name': 'Loveth',
            'last_name': 'Ubah',
            'username': 'sdominic',
            'vehicle_number': 'sRaymond',
            'email': 'aymond@gmail.com',
            'password': '112345',
            'phone_number': '233455632',
            'status': 'i no dey here',
            'file': file
            }
            headers = {'Content-Type': 'multipart/form-data'}
            response = self.client.post('/api/register', data=data2, headers=headers)
        data = response.json
        self.assertEqual(response.status_code, 400)
        self.assertFalse('username' in data)

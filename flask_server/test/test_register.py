import unittest
from flask_testing import TestCase
from flask import Flask
from ..app import db
from ..views.v1 import app_views

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
    def test_signup(self):
        with self.client:
            data2 = {
            'username': 'sdominic',
            'vehicle_number': 'sRaymond',
            'email': 'aymond@gmail.com',
            'password': '112345',
            'confirm_password': '112345',
            'phone_number': '233455632'
            }
            response = self.client.post('/api/register', data=data2)
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertTrue('username' in data)
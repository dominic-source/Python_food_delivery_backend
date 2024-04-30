import unittest
from flask_testing import TestCase
from flask import Flask
from ..app import db
from ..views.v1 import app_views
import os

class TestUser(TestCase):
	"""This class is meant to test cases that has to do with the user"""

	def create_app(self):
		self.app = Flask(__name__)
		self.app.config['TESTING'] = True
		self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
		self.app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
		self.app.register_blueprint(app_views)
		db.init_app(self.app)
		with self.app.app_context():
			db.create_all()
		return self.app

	def tearDown(self):
		with self.app.app_context():
			db.session.remove()
			db.drop_all()

	def test_update_user(self):
		with self.client:
			data2 = {
			'first_name': 'sylveth',
			'last_name': 'monh',
			'username': 'sdominic',
			'vehicle_number': 'sRaymond',
			'email': 'aymond@gmail.com',
			'password': '112345',
			'phone_number': '233455632',
			'status': 'busy',
			}
			headers = {'Content-Type': 'multipart/form-data'}
			self.client.post('/api/register', data=data2, headers=headers)
			data3 = {
				'email': 'aymond@gmail.com',
				'password': '112345'
			}
			response = self.client.post('/api/login', data=data3, headers=headers)
		self.assertEqual(response.status_code, 200)
		self.assertEqual('User log in successful', response.text)
		data4 = {
			'first_name': 'Emmanuel'
		}
		resp = self.client.post('/api/update_user', data=data4, headers=headers)
		self.assertEqual(response.status_code, 200)
		self.assertEqual('user profile updated successfullly', resp.json['data'])
		self.assertFalse(resp.json.get('error', None))

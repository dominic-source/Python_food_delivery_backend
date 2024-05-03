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
		import queue
		queue = queue.Queue()
		db.init_app(self.app)
		with self.app.app_context():
			db.create_all()
		return self.app

	def tearDown(self):
		with self.app.app_context():
			db.session.remove()
			db.drop_all()

	def test_forgot_password(self):
		with self.client:
			data2 = {
			'first_name': 'Loveth',
			'last_name': 'Ubah',
			'username': 'sdominic',
			'vehicle_number': 'sRaymond',
			'email': 'dominicmorba@gmail.com',
			'password': '112345',
			'phone_number': '233455632',
			'status': 'busy',
			}
			headers = {'Content-Type': 'multipart/form-data'}
			self.client.post('/api/register', data=data2, headers=headers)
			data3 = {
				'email': 'dominicmorba@gmail.com',
				'password': '112345'
			}
			response = self.client.post('/api/forgot_password', data=data3, headers=headers)
			token = response.json.get('success', None)
			data4 = {
				'email': 'dominicmorba@gmail.com',
				'password': 'domnic',
				'token': token
			}
			# response2 = self.client.post('/api/update_password',data=data4, headers=headers)
			# response3 = self.client.post('/api/login', data=data4, headers=headers)
			# response4 = self.client.post('/api/login', data=data3, headers=headers)

		self.assertEqual(response.status_code, 200)
		# self.assertEqual(response2.json['success'], 'password updated successfully')
		# self.assertEqual(response3.text, 'User log in successful')
		# self.assertEqual(response3.status_code, 200)
		# self.assertNotEqual(response4.status_code, 200)

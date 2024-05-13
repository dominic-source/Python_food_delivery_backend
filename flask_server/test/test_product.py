import unittest
from flask_testing import TestCase
from flask import Flask
from .. import app_views, db
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

	def setUp(self):
		with self.client:
			data2 = {
			'first_name': 'oveth',
			'last_name': 'Ubah',
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
			self.client.post('/api/login', data=data3, headers=headers)

			data5 = {
                'name': 'Consumable Products | Food & Beverages | Staples (Rice, Flour, Pasta)'
            }
			self.client.post('/api/category', data=data5)
			data4 = {
                'name': 'Custard milk',
                'description': 'description',
                'price': 1200,
                'currency': 'Naira', 
                'category_id': 1,
                'quantity': 20,
                'user_id': 1
            }
			self.response = self.client.post('/api/product', data=data4)

	def test_create_product(self):
		self.assertEqual(self.response.status_code, 200)

	def test_delete_product(self):
		with self.client:
			resp = self.client.delete(f"api/product/{self.response.json['id']}")
		self.assertEqual(resp.status_code, 200)

	def test_get_product(self):
		with self.client:
			resp = self.client.get(f"api/product/{self.response.json['id']}")
		self.assertEqual(resp.status_code, 200)

	def test_get_all_product(self):
		with self.client:
			data6 = {
                'name': 'Custard milk and breweries',
                'description': 'description',
                'price': 1200,
                'currency': 'Naira', 
                'category_id': 1,
                'quantity': 20,
                'user_id': 1
            }
			self.client.post('/api/product', data=data6)

			resp = self.client.get("api/products")
		self.assertEqual(resp.status_code, 200)


	def test_get_users_products(self):
		with self.client:
			data6 = {
                'name': 'Custard milk and breweries',
                'description': 'description',
                'price': 1200,
                'currency': 'Naira', 
                'category_id': 1,
                'quantity': 20,
                'user_id': 1
            }
			self.client.post('/api/product', data=data6)
			resp = self.client.get("api/products/users")
		self.assertEqual(resp.status_code, 200)

	def test_get_categories_products(self):
		with self.client:
			data6 = {
                'name': 'Custard milk',
                'description': 'description',
                'price': 1200,
                'currency': 'Naira', 
                'category_id': 1,
                'quantity': 20,
                'user_id': 1
            }
			self.client.post('/api/product', data=data6)
			resp = self.client.get("api/products/categories/1")
		self.assertEqual(resp.status_code, 200)


	def test_update_product(self):
		with self.client:
			data6 = {
                'name': 'Custard milk and breweries',
                'price': 1300,
                'currency': 'Dollar', 
                'category_id': 1,
                'quantity': 20,
                'user_id': 1
            }
			resp = self.client.put(f'/api/product/{self.response.json["id"]}', data=data6)
		self.assertEqual(resp.status_code, 200)
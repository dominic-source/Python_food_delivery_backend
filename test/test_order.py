import unittest
from flask_testing import TestCase
from flask import Flask
from .. import db
from ..views.v1 import app_views
import json
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
			'username': 'admin',
			'vehicle_number': 'sRaymond',
			'email': 'admin@deliver.com',
			'password': '112345',
			'phone_number': '233455632',
			'status': 'busy',
			}
			headers = {'Content-Type': 'multipart/form-data'}
			self.client.post('/api/register', data=data2, headers=headers)
			data3 = {
				'email': 'admin@deliver.com',
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

	def test_create_order(self):
		with self.client:
			data = {
                'seller_id': 1,
                'dispatcher_id': 1,
                'delivery_address': 'myaddress',
                'orderitems': [
                    {
                        'product_id': 1,
                        'quantity': 2
                    },
                    {
                        'product_id': 1,
                        'quantity': 3
                    }
                ]

            }
			header = {'Content-Type': 'application/json'}
			resp = self.client.post(f"api/order", headers=header, json=json.dumps(data))
			self.assertEqual(resp.status_code, 201)
		
	def test_get_order(self):
		"""This tests the get_order views"""
		data = {
                'seller_id': 1,
                'dispatcher_id': 1,
                'delivery_address': 'myaddress',
                'orderitems': [
                    {
                        'product_id': 1,
                        'quantity': 2
                    },
                    {
                        'product_id': 1,
                        'quantity': 3
                    }
                ]
            }
		header = {'Content-Type': 'application/json'}
		self.client.post(f"api/order", headers=header, json=json.dumps(data))
		self.client.post(f"api/order", headers=header, json=json.dumps(data))
		resp = self.client.post(f"api/order", headers=header, json=json.dumps(data))
		# id = resp.json['order_id']
		response = self.client.get('/api/my_orders?seller=true')
		self.assertEqual(response.status_code, 200)

	def test_all_order(self):
		"""This tests the get_order views"""
		data = {
                'seller_id': 1,
                'dispatcher_id': 1,
                'delivery_address': 'myaddress',
                'orderitems': [
                    {
                        'product_id': 1,
                        'quantity': 2
                    },
                    {
                        'product_id': 1,
                        'quantity': 3
                    }
                ]
            }
		header = {'Content-Type': 'application/json'}
		self.client.post(f"api/order", headers=header, json=json.dumps(data))
		self.client.post(f"api/order", headers=header, json=json.dumps(data))
		response = self.client.get('/api/all_orders')
		self.assertEqual(response.status_code, 200)

	def test_get_all_items_of_order(self):
		"""This tests the get_order views"""
		data = {
                'seller_id': 1,
                'dispatcher_id': 1,
                'delivery_address': 'myaddress',
                'orderitems': [
                    {
                        'product_id': 1,
                        'quantity': 2
                    },
                    {
                        'product_id': 1,
                        'quantity': 3
                    }
                ]
            }
		header = {'Content-Type': 'application/json'}
		self.client.post(f"api/order", headers=header, json=json.dumps(data))
		self.client.post(f"api/order", headers=header, json=json.dumps(data))
		resp = self.client.post(f"api/order", headers=header, json=json.dumps(data))
		response = self.client.get(f"/api/order_items/{resp.json['order_id']}")
		self.assertEqual(response.status_code, 200)

	def test_get_all_items_of_order_with_errors(self):
		"""This tests the get_order views"""
		data = {
                'seller_id': 1,
                'dispatcher_id': 1,
                'delivery_address': 'myaddress',
                'orderitems': [
                    {
                        'product_id': 1,
                        'quantity': 2
                    },
                    {
                        'product_id': 1,
                        'quantity': 3
                    }
                ]
            }
		header = {'Content-Type': 'application/json'}
		self.client.post(f"api/order", headers=header, json=json.dumps(data))
		self.client.post(f"api/order", headers=header, json=json.dumps(data))
		resp = self.client.post(f"api/order", headers=header)
		response = self.client.get(f"/api/order_items/{resp.json.get('order_id')}")
		self.assertEqual(response.status_code, 404)

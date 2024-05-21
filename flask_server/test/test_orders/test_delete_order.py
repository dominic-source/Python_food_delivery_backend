import unittest
from flask_testing import TestCase
from flask import Flask
from ... import db
from ...views.v1 import app_views
import json

class TestDeleteAndUpdateOrder(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SECRET_KEY'] = 'SECRET_KEY'
        app.register_blueprint(app_views)
        self.db = db.init_app(app)
        with app.app_context():
            db.create_all()
        return app

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
            data2 = {
                'seller_id': 2,
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
            self.client.post(f"api/order", headers=header, json=json.dumps(data2))

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_delete_order_success(self):
        with self.client:
            response = self.client.delete('/api/order/1')
            self.assertEqual(response.status_code, 200)
            print(response.json)
            self.assertEqual(response.json, {'message': 'order deleted successfully'})

    def test_delete_order_not_found(self):
        with self.client:
            response = self.client.delete('/api/order/99')
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json, {'message': 'order not found!'})
    
    def test_update_order(self):
        with self.client:
            data = {
                'order_id': 1,
                'delivery_address': 'Itapa'
            }
            response = self.client.put('/api/order', data=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'message': 'order updated successfully'})

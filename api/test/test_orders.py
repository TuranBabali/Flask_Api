import unittest
from flask_jwt_extended import create_access_token

from api import create_app
from api.config.config import config_dict
from api.orders.orders import Order
from api.utils import db


class OrderTestCase(unittest.TestCase):
    def setUp(self):
        self.app=create_app(config=config_dict['test'])
        self.appctx=self.app.app_context()
        self.appctx.push()
        self.client=self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()
        self.app=None
        self.appctx.pop()
        self.client=None

    def test_get_all_orders(self):

        token=create_access_token(identity='testuser')

        headers={
            "Authorization":f"Bearer {token}"
        }
        response=self.client.get('/orders/orders', headers=headers)

        assert response.status_code ==200
        assert response.json==[]


    def test_create_order(self):
        data={
               "size":"LARGE",
                "quantity":3,
                "flavour": "Test Flovour"

            }
        token=create_access_token(identity='testuser')

        headers={
        "Authorization":f"Bearer {token}"
        }
        response=self.client.post('/orders/orders', json=data, headers=headers)

        assert response.status_code == 201
        orders=Order.query.all()

        assert len(orders) == 1 
            
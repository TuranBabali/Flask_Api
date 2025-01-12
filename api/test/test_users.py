import unittest
from werkzeug.security import generate_password_hash

from api import create_app
from api.config.config import config_dict
from api.utils import db
from api.orders.orders import User


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app=create_app(config=config_dict['test'])
        self.appctx=self.app.app_context()
        self.appctx.push()
        self.client=self.app.test_client()

        db.create_all()

    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app=None
        self.client=None

    def test_user_registrtration(self):
        data={
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password": "password"
        }
        response=self.client.post('/auth/signup', json=data)

        user=User.query.filter_by(email="testuser@gmail.com").first()

        assert user.username =="testuser"

        assert response.status_code == 201

    def test_login(self):
        
        data={
            "email":"testuser@gmail.com",
            "password": "password"
        }
        response=self.client.post('/auth/login', json=data)

        assert response.status_code == 400


        
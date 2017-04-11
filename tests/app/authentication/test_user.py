import unittest

from flask import Flask

from app import settings
from app.authentication.user import User


class TestUser(unittest.TestCase):

    def setUp(self):
        self.application = Flask(__name__)
        self.application.config['TESTING'] = True
        settings.EQ_SERVER_SIDE_STORAGE = True

    def test_get_user_id(self):
        with self.application.test_request_context():
            user = User("1", "2")
            self.assertEqual("1", user.user_id)

    def test_get_user_ik(self):
        with self.application.test_request_context():
            user = User("1", "2")
            self.assertEqual("2", user.user_ik)

    def test_negative_user(self):
        with self.application.test_request_context():
            user = User("-1", "2")
            self.assertEqual("-1", user.user_id)

    def test_no_user(self):
        with self.application.test_request_context():
            with self.assertRaises(ValueError):
                User("", "")

    def test_none_user(self):
        with self.application.test_request_context():
            with self.assertRaises(ValueError):
                User(None, "2")

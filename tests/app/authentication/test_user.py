import unittest
from app.authentication.user import User
from app import settings
from flask import Flask


class TestUser(unittest.TestCase):

    def setUp(self):
        self.application = Flask(__name__)
        self.application.config['TESTING'] = True
        settings.EQ_SERVER_SIDE_STORAGE = True

    def test_get_user_id(self):
        with self.application.test_request_context():
            user = User("1", "2")
            self.assertEquals("1", user.user_id)

    def test_get_user_ik(self):
        with self.application.test_request_context():
            user = User("1", "2")
            self.assertEquals("2", user.user_ik)


import unittest
from app.authentication.user import User
from flask import Flask


class TestUser(unittest.TestCase):

    def setUp(self):
        self.application = Flask(__name__)
        self.application.config['TESTING'] = True

    def test_get_user_id(self):
        with self.application.test_request_context():
            user = User("1")
            self.assertEquals("1", user.get_user_id())



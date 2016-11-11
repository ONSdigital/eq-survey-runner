from app.authentication.session_manager import SessionManager
from flask import Flask
import unittest
from datetime import timedelta
from app import settings


class BaseSessionManagerTest(unittest.TestCase):
    def setUp(self):
        application = Flask(__name__)
        application.config['TESTING'] = True
        application.secret_key = 'you will not guess'
        application.permanent_session_lifetime = timedelta(seconds=1)
        self.application = application
        # Use an in memory database
        settings.EQ_SERVER_SIDE_STORAGE_DATABASE_URL = "sqlite://"
        self.session_manager = SessionManager()

    def test_has_token_empty(self):
        with self.application.test_request_context():
            self.assertFalse(self.session_manager.has_user_id())

    def test_has_token(self):
        with self.application.test_request_context():
            self.session_manager.store_user_id("test")
            self.assertTrue(self.session_manager.has_user_id())

    def test_remove_token(self):
        with self.application.test_request_context():
            self.session_manager.store_user_id("test")
            self.assertTrue(self.session_manager.has_user_id())
            self.session_manager.clear()
            self.assertFalse(self.session_manager.has_user_id())


if __name__ == '__main__':
    unittest.main()

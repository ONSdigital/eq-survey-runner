from app.authentication.session_management import FlaskSessionManager
from flask import Flask
import unittest
from datetime import timedelta


class FlaskSessionManagerTest(unittest.TestCase):

    def setUp(self):
        application = Flask(__name__)
        application.config['TESTING'] = True
        application.secret_key = 'you will not guess'
        application.permanent_session_lifetime = timedelta(seconds=1)
        self.application = application

    def test_has_token_empty(self):
        with self.application.test_request_context():
            session_manager = FlaskSessionManager()
            self.assertFalse(session_manager.has_user_id())

    def test_has_token(self):
        with self.application.test_request_context():
            session_manager = FlaskSessionManager()
            session_manager.store_user_id("test")
            self.assertTrue(session_manager.has_user_id())

    def test_remove_token(self):
        with self.application.test_request_context():
            session_manager = FlaskSessionManager()
            session_manager.store_user_id("test")
            self.assertTrue(session_manager.has_user_id())
            session_manager.remove_user_id()
            self.assertFalse(session_manager.has_user_id())

if __name__ == '__main__':
    unittest.main()

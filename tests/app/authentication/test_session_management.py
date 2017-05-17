import unittest
from datetime import timedelta

from flask import Flask

from app import Database
from app.authentication.session_storage import SessionStorage


class BaseSessionManagerTest(unittest.TestCase):
    def setUp(self):
        application = Flask(__name__)
        application.config['TESTING'] = True
        application.secret_key = 'you will not guess'
        application.permanent_session_lifetime = timedelta(seconds=1)
        self.application = application
        # Use an in memory database
        self.database = Database("sqlite://", 1, 0)
        self.session_manager = SessionStorage(self.database)

    def test_has_token_empty(self):
        with self.application.test_request_context():
            self.assertIsNone(self.session_manager.get_user_id())

    def test_has_token(self):
        with self.application.test_request_context():
            self.session_manager.store_user_id("test")
            self.assertIsNotNone(self.session_manager.get_user_id())

    def test_remove_token(self):
        with self.application.test_request_context():
            self.session_manager.store_user_id("test")
            self.assertIsNotNone(self.session_manager.get_user_id())
            self.session_manager.delete_session_from_db()
            self.assertIsNone(self.session_manager.get_user_id())

    def test_remove_user_ik(self):
        with self.application.test_request_context():
            self.session_manager.remove_user_ik()
            self.assertIsNone(self.session_manager.get_user_ik())

if __name__ == '__main__':
    unittest.main()

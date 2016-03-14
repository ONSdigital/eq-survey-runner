from app.navigation.navigation_history import FlaskNavigationHistory
from datetime import timedelta
from flask import Flask
import unittest


class FlaskNavigationHistoryTest(unittest.TestCase):

    def setUp(self):
        application = Flask(__name__)
        application.config['TESTING'] = True
        application.secret_key = 'you will not guess'
        application.permanent_session_lifetime = timedelta(seconds=1)
        self.application = application

    def test_add_history(self):
        with self.application.test_request_context():
            navigation_history = FlaskNavigationHistory()
            navigation_history.add_history_entry("test1")
            self.assertIn("test1", navigation_history.get_history())

    def test_add_more_history(self):
        with self.application.test_request_context():
            navigation_history = FlaskNavigationHistory()
            navigation_history.add_history_entry("test1")
            self.assertIn("test1", navigation_history.get_history())
            navigation_history.add_history_entry("test2")
            self.assertIn("test1", navigation_history.get_history())
            self.assertIn("test2", navigation_history.get_history())

if __name__ == '__main__':
    unittest.main()

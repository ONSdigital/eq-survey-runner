from app.navigation.navigator import Navigator
from app.navigation.navigation_history import FlaskNavigationHistory
from datetime import timedelta
from flask import Flask
import unittest


class NavigatorTest(unittest.TestCase):
    def setUp(self):
        application = Flask(__name__)
        application.config['TESTING'] = True
        application.secret_key = 'you will not guess'
        application.permanent_session_lifetime = timedelta(seconds=1)
        self.application = application

    def test_get_current_location(self):
        with self.application.test_request_context():
            schema = {}
            navigation_history = FlaskNavigationHistory()
            navigator = Navigator(schema, navigation_history)
            #  brand new session shouldn't have a current location
            self.assertIsNone(navigator.get_current_location())

    def test_go_to(self):
        with self.application.test_request_context():
            schema = {}
            navigation_history = FlaskNavigationHistory()
            navigator = Navigator(schema, navigation_history)
            navigator.go_to("completed")
            self.assertEquals("completed", navigator.get_current_location())

if __name__ == '__main__':
    unittest.main()

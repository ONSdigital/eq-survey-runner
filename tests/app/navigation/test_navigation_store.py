from app.navigation.navigation_store import FlaskNavigationStore
from app.navigation.navigation_state import NavigationState
from datetime import timedelta
from flask import Flask
import unittest


class FlaskNavigationStoreTest(unittest.TestCase):

    def setUp(self):
        application = Flask(__name__)
        application.config['TESTING'] = True
        application.secret_key = 'you will not guess'
        application.permanent_session_lifetime = timedelta(seconds=1)
        self.application = application

    def test_add_history(self):
        with self.application.test_request_context():
            navigation_store = FlaskNavigationStore()
            navigation_state = NavigationState()
            navigation_state.current_position = "start"
            navigation_store.store_state(navigation_state)
            self.assertEquals("start", navigation_store.get_state().current_position)

if __name__ == '__main__':
    unittest.main()

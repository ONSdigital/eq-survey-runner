import unittest

from app.setup import create_app
from app.storage import data_access


class AppContextTestCase(unittest.TestCase):
    """
    unittest.TestCase that creates a Flask app context on setUp
    and destroys it on tearDown
    """
    LOGIN_DISABLED = False

    def setUp(self):
        setting_overrides = {
            'SQLALCHEMY_DATABASE_URI': 'sqlite://',
            'LOGIN_DISABLED': self.LOGIN_DISABLED,
            'EQ_DYNAMODB_ENABLED': True,
            'EQ_DYNAMODB_ENDPOINT': 'http://localhost:6060',
        }
        self._app = create_app(setting_overrides)

        self._app.config['SERVER_NAME'] = 'test'
        self._app_context = self._app.app_context()
        self._app_context.push()

    def tearDown(self):
        with self._app.app_context():
            data_access.flush_all_data()

        self._app_context.pop()

    def test_request_context(self, *args, **kwargs):
        return self._app.test_request_context(*args, **kwargs)

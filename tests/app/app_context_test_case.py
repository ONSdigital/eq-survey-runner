import unittest

from app import create_app


class AppContextTestCase(unittest.TestCase):
    """
    unittest.TestCase that creates a Flask app context on setUp
    and destroys it on tearDown
    """
    def setUp(self):
        setting_overrides = {
            "EQ_SERVER_SIDE_STORAGE_DATABASE_URL": "sqlite://"
        }
        self._app = create_app(setting_overrides)
        self._app.config['SERVER_NAME'] = 'test'
        self._app_context = self._app.app_context()
        self._app_context.push()

    def tearDown(self):
        self._app_context.pop()

    def test_request_context(self, *args, **kwargs):
        return self._app.test_request_context(*args, **kwargs)

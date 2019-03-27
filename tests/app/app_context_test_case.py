import contextlib
import unittest

from google.cloud.datastore import Key
from mock import patch

from app.setup import create_app


class MockDatastore:

    # pylint: disable=unused-argument
    def __init__(self, **kwargs):
        self.storage = {}

    # pylint: disable=no-self-use
    def transaction(self):
        return contextlib.suppress()

    def put(self, entity):
        self.storage[entity.key] = entity

    def get(self, key):
        return self.storage.get(key)

    def delete(self, key):
        del self.storage[key]

    # pylint: disable=no-self-use
    def key(self, *path_args, **kwargs):
        return Key(*path_args, project='local', **kwargs)


class AppContextTestCase(unittest.TestCase):
    """
    unittest.TestCase that creates a Flask app context on setUp
    and destroys it on tearDown
    """
    LOGIN_DISABLED = False
    setting_overrides = {}

    def setUp(self):
        self._ds = patch('app.setup.datastore.Client', MockDatastore)
        self._ds.start()

        setting_overrides = {
            'LOGIN_DISABLED': self.LOGIN_DISABLED,
        }
        setting_overrides.update(self.setting_overrides)
        self._app = create_app(setting_overrides)

        self._app.config['SERVER_NAME'] = 'test.localdomain'
        self._app_context = self._app.app_context()
        self._app_context.push()

    def tearDown(self):
        self._app_context.pop()

    def app_request_context(self, *args, **kwargs):
        return self._app.test_request_context(*args, **kwargs)

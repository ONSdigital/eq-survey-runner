from app.storage.memory_storage import InMemoryStorage
from app.storage.database_storage import DatabaseStorage
from app.storage.session_storage import FlaskSessionStore
from app import settings
from datetime import timedelta
from flask import Flask
import unittest

USER_ID = "1"


class BaseTestStorage(unittest.TestCase):

    def setUp(self):
        self.storage = InMemoryStorage()

    def tearDown(self):
        # always clear out the memory between test runs
        self.storage.clear()

    def test_store(self):
        data = {'test': 'test'}
        self.assertIsNone(self.storage.store(USER_ID, data))
        self.assertTrue(self.storage.has_data(USER_ID))

    def test_get(self):
        data = {'test': 'test'}
        self.storage.store(USER_ID, data)
        self.assertEqual(data, self.storage.get(USER_ID))

    def test_delete(self):
        data = {'test': 'test'}
        self.storage.store(USER_ID, data)
        self.assertEqual(data, self.storage.get(USER_ID))
        self.storage.delete(USER_ID)
        self.assertFalse(self.storage.has_data(USER_ID))
        self.assertIsNone(self.storage.get(USER_ID))

    def test_clear(self):
        data = {'test': 'test'}
        self.storage.store(USER_ID, data)
        self.assertEqual(data, self.storage.get(USER_ID))
        self.storage.clear()
        self.assertFalse(self.storage.has_data(USER_ID))
        self.assertIsNone(self.storage.get(USER_ID))


class TestInMemoryStorage(BaseTestStorage):

    def setUp(self):
        self.storage = InMemoryStorage()


class TestDatabaseStorage(BaseTestStorage):

    def setUp(self):
        # use an inmemory database
        settings.EQ_SERVER_SIDE_STORAGE_DATABASE_URL = "sqlite://"
        self.storage = DatabaseStorage()


class TestFlaskSessionStorage(BaseTestStorage):

    def setUp(self):
        self.application = Flask(__name__)
        self.application.config['TESTING'] = True
        self.storage = FlaskSessionStore()
        self.application.secret_key = 'you will not guess'
        self.application.permanent_session_lifetime = timedelta(seconds=1)

    def tearDown(self):
        pass

    def test_store(self):
        with self.application.test_request_context():
            super().test_store()

    def test_get(self):
        with self.application.test_request_context():
            super().test_get()

    def test_delete(self):
        with self.application.test_request_context():
            super().test_delete()

    def test_clear(self):
        with self.application.test_request_context():
            super().test_clear()


if __name__ == '__main__':
    unittest.main()

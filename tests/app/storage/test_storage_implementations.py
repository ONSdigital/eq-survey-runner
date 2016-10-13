from app.storage.database_storage import DatabaseStorage
from app import settings
import unittest


class TestDatabaseStorage(unittest.TestCase):

    def setUp(self):
        # use an inmemory database
        settings.EQ_SERVER_SIDE_STORAGE_DATABASE_URL = "sqlite://"
        self.storage = DatabaseStorage()

    def tearDown(self):
        # always clear out the memory between test runs
        self.storage.clear()

    def test_store(self):
        data = {'test': 'test'}
        self.assertIsNone(self.storage.store(data, "1", "2"))
        self.assertTrue(self.storage.has_data("1"))

    def test_get(self):
        data = {'test': 'test'}
        self.storage.store(data, "1", "2")
        self.assertEqual(data, self.storage.get("1", "2"))

    def test_delete(self):
        data = {'test': 'test'}
        self.storage.store(data, "1", "2")
        self.assertEqual(data, self.storage.get("1", "2"))
        self.storage.delete("1")
        self.assertFalse(self.storage.has_data("1"))
        self.assertIsNone(self.storage.get("1", "2"))

    def test_clear(self):
        data = {'test': 'test'}
        self.storage.store(data, "1", "2")
        self.assertEqual(data, self.storage.get("1", "2"))
        self.storage.clear()
        self.assertFalse(self.storage.has_data("1"))
        self.assertIsNone(self.storage.get("1", "2"))

if __name__ == '__main__':
    unittest.main()

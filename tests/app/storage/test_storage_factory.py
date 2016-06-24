from app import settings
from app.storage.storage_factory import StorageFactory
from app.storage.memory_storage import InMemoryStorage
from app.storage.encrypted_storage import EncryptedServerStorageDecorator
from app.storage.database_storage import DatabaseStorage
import unittest


class TestStorageFactory(unittest.TestCase):

    def test_in_memory_storage(self):
        settings.EQ_SERVER_SIDE_STORAGE_TYPE = "memory"
        settings.EQ_SERVER_SIDE_STORAGE_ENCRYPTION = False
        self.assertIsInstance(StorageFactory.get_storage_mechanism(), InMemoryStorage)

    def test_database_storage(self):
        settings.EQ_SERVER_SIDE_STORAGE_TYPE = "database"
        settings.EQ_SERVER_SIDE_STORAGE_ENCRYPTION = False
        self.assertIsInstance(StorageFactory.get_storage_mechanism(), DatabaseStorage)

    def test_encrypted_storage(self):
        settings.EQ_SERVER_SIDE_STORAGE_TYPE = "database"
        settings.EQ_SERVER_SIDE_STORAGE_ENCRYPTION = True
        self.assertIsInstance(StorageFactory.get_storage_mechanism(), EncryptedServerStorageDecorator)

if __name__ == '__main__':
    unittest.main()

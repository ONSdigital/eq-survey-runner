from app import settings
from app.storage.storage_factory import get_storage
from app.storage.encrypted_storage import EncryptedStorage
from app.storage.database_storage import DatabaseStorage
import unittest


class TestStorageFactory(unittest.TestCase):

    def test_database_storage(self):
        settings.EQ_SERVER_SIDE_STORAGE_TYPE = "database"
        settings.EQ_SERVER_SIDE_STORAGE_ENCRYPTION = False
        self.assertIsInstance(get_storage(), DatabaseStorage)

    def test_encrypted_storage(self):
        settings.EQ_SERVER_SIDE_STORAGE_TYPE = "database"
        settings.EQ_SERVER_SIDE_STORAGE_ENCRYPTION = True
        self.assertIsInstance(get_storage(), EncryptedStorage)

if __name__ == '__main__':
    unittest.main()

from app.storage.encrypted_storage import EncryptedStorageDecorator
from app.storage.database_storage import DatabaseStorage
from app.authentication.user_id_generator import UserIDGenerator
from app import settings


import unittest


class TestEncryptedServerStorageDecorator(unittest.TestCase):

    def test_generate_cek(self):
        encrypted = EncryptedStorageDecorator(DatabaseStorage())
        cek1 = encrypted._generate_key("user1", "user_ik_1")
        cek2 = encrypted._generate_key("user1", "user_ik_1")
        cek3 = encrypted._generate_key("user2", "user_ik_2")
        self.assertEquals(cek1, cek2)
        self.assertNotEquals(cek1, cek3)
        self.assertNotEquals(cek2, cek3)

    def test_generate_cek_different_user_ids(self):
        encrypted = EncryptedStorageDecorator(DatabaseStorage())
        cek1 = encrypted._generate_key("user1", "user_ik_1")
        cek2 = encrypted._generate_key("user1", "user_ik_1")
        cek3 = encrypted._generate_key("user2", "user_ik_1")
        self.assertEquals(cek1, cek2)
        self.assertNotEquals(cek1, cek3)
        self.assertNotEquals(cek2, cek3)

    def test_generate_cek_different_user_iks(self):
        encrypted = EncryptedStorageDecorator(DatabaseStorage())
        cek1 = encrypted._generate_key("user1", "user_ik_1")
        cek2 = encrypted._generate_key("user1", "user_ik_1")
        cek3 = encrypted._generate_key("user1", "user_ik_2")
        self.assertEquals(cek1, cek2)
        self.assertNotEquals(cek1, cek3)
        self.assertNotEquals(cek2, cek3)

    def test_generate_cek_different_pepper(self):
        encrypted = EncryptedStorageDecorator(DatabaseStorage())
        cek1 = encrypted._generate_key("user1", "user_ik_1")
        settings.EQ_SERVER_SIDE_STORAGE_ENCRYPTION_KEY_PEPPER = "test"
        cek2 = encrypted._generate_key("user1", "user_ik_1")
        self.assertNotEquals(cek1, cek2)

    def test_generate_cek_different_pepper(self):
        encrypted = EncryptedStorageDecorator(DatabaseStorage())
        cek1 = encrypted._generate_key("user1", "user_ik_1")
        settings.EQ_SERVER_SIDE_STORAGE_ENCRYPTION_KEY_PEPPER = "test"
        cek2 = encrypted._generate_key("user1", "user_ik_1")
        self.assertNotEquals(cek1, cek2)

    def test_store_and_get(self):
        storage = DatabaseStorage()
        encrypted = EncryptedStorageDecorator(storage)
        user_id = '1'
        user_ik = '2'
        data = "test"
        encrypted.store(data, user_id, user_ik)
        # check we can decrypt the data
        self.assertEquals(data, encrypted.get(user_id, user_ik))

        # check the underlying store has the encrypted version
        self.assertIsNotNone(storage.get(user_id))
        self.assertNotEquals(data, storage.get(user_id))

if __name__ == '__main__':
    unittest.main()

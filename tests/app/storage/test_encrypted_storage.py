from app.storage.encrypted_storage import EncryptedServerStorageDecorator
from app.storage.memory_storage import InMemoryStorage


import unittest


class TestEncryptedServerStorageDecorator(unittest.TestCase):

    def test_generate_cek(self):
        encrypted = EncryptedServerStorageDecorator(InMemoryStorage())
        cek1 = encrypted._generate_key("user1")
        cek2 = encrypted._generate_key("user1")
        cek3 = encrypted._generate_key("user2")
        self.assertEquals(cek1, cek2)
        self.assertNotEquals(cek1, cek3)
        self.assertNotEquals(cek2, cek3)

    def test_store_and_get(self):
        storage = InMemoryStorage()
        encrypted = EncryptedServerStorageDecorator(storage)
        user_id = '1'
        data = "test"
        encrypted.store(user_id, data)
        # check we can decrypt the data
        self.assertEquals(data, encrypted.get(user_id))

        # check the underlying store has the encrypted version
        self.assertIsNotNone(storage.get(user_id))
        self.assertNotEquals(data, storage.get(user_id))

if __name__ == '__main__':
    unittest.main()

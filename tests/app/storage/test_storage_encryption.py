from unittest import TestCase
import simplejson as json

from app.storage.storage_encryption import StorageEncryption

# pylint: disable=W0212
class TestStorageEncryption(TestCase):

    def setUp(self):
        super().setUp()
        self.encrypter = StorageEncryption('user_id', 'user_ik', 'pepper')

    def test_encrypted_storage_requires_user_id(self):
        with self.assertRaises(ValueError):
            StorageEncryption(None, 'key', 'pepper')

    def test_encrypted_storage_requires_user_ik(self):
        with self.assertRaises(ValueError):
            StorageEncryption('1', None, 'pepper')

    def test_generate_key(self):
        key1 = StorageEncryption('user1', 'user_ik_1', 'pepper').key._key['k']
        key2 = StorageEncryption('user1', 'user_ik_1', 'pepper').key._key['k']
        key3 = StorageEncryption('user2', 'user_ik_2', 'pepper').key._key['k']
        self.assertEqual(key1, key2)
        self.assertNotEqual(key1, key3)
        self.assertNotEqual(key2, key3)

    def test_generate_key_different_user_ids(self):
        key1 = StorageEncryption('user1', 'user_ik_1', 'pepper').key._key['k']
        key2 = StorageEncryption('user1', 'user_ik_1', 'pepper').key._key['k']
        key3 = StorageEncryption('user2', 'user_ik_1', 'pepper').key._key['k']
        self.assertEqual(key1, key2)
        self.assertNotEqual(key1, key3)
        self.assertNotEqual(key2, key3)

    def test_generate_key_different_user_iks(self):
        key1 = StorageEncryption('user1', 'user_ik_1', 'pepper').key._key['k']
        key2 = StorageEncryption('user1', 'user_ik_1', 'pepper').key._key['k']
        key3 = StorageEncryption('user1', 'user_ik_2', 'pepper').key._key['k']
        self.assertEqual(key1, key2)
        self.assertNotEqual(key1, key3)
        self.assertNotEqual(key2, key3)

    def test_encryption_decryption(self):
        data = {
            'data1': 'Test Data One',
            'data2': 'Test Data Two'
        }
        encrypted_data = self.encrypter.encrypt_data(data)
        self.assertNotEqual(encrypted_data, data)
        self.assertIsInstance(encrypted_data, str)

        decrypted_data = self.encrypter.decrypt_data(encrypted_data)
        decrypted_data = json.loads(decrypted_data)
        self.assertEqual(data, decrypted_data)

    def test_no_pepper(self):
        with self.assertRaises(ValueError):
            self.encrypter = StorageEncryption('user_id', 'user_ik', None)

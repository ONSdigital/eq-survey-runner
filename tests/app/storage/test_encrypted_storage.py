from app.storage.encrypted_storage import EncryptedServerStorageDecorator

import unittest


class TestEncryptedServerStorageDecorator(unittest.TestCase):

    def test_generate_cek(self):
        encrypted = EncryptedServerStorageDecorator()
        cek1 = encrypted._generate_key("user1")
        cek2 = encrypted._generate_key("user1")
        cek3 = encrypted._generate_key("user2")
        self.assertEquals(cek1, cek2)
        self.asserNottEquals(cek1, cek3)
        self.asserNottEquals(cek2, cek3)

if __name__ == '__main__':
    unittest.main()

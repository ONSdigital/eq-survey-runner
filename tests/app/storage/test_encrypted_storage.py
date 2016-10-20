from app.storage.encrypted_storage import EncryptedStorage, generate_key


import unittest


class TestEncryptedStorage(unittest.TestCase):

    def test_generate_cek(self):
        cek1 = generate_key("user1", "user_ik_1")
        cek2 = generate_key("user1", "user_ik_1")
        cek3 = generate_key("user2", "user_ik_2")
        self.assertEquals(cek1, cek2)
        self.assertNotEquals(cek1, cek3)
        self.assertNotEquals(cek2, cek3)

    def test_generate_cek_different_user_ids(self):
        cek1 = generate_key("user1", "user_ik_1")
        cek2 = generate_key("user1", "user_ik_1")
        cek3 = generate_key("user2", "user_ik_1")
        self.assertEquals(cek1, cek2)
        self.assertNotEquals(cek1, cek3)
        self.assertNotEquals(cek2, cek3)

    def test_generate_cek_different_user_iks(self):
        cek1 = generate_key("user1", "user_ik_1")
        cek2 = generate_key("user1", "user_ik_1")
        cek3 = generate_key("user1", "user_ik_2")
        self.assertEquals(cek1, cek2)
        self.assertNotEquals(cek1, cek3)
        self.assertNotEquals(cek2, cek3)

    def test_generate_cek_different_pepper(self):
        cek1 = generate_key("user1", "user_ik_1")
        cek2 = generate_key("user1", "user_ik_1", "test")
        self.assertNotEquals(cek1, cek2)

    def test_store_and_get(self):
        encrypted = EncryptedStorage()
        user_id = '1'
        user_ik = '2'
        data = "test"
        encrypted.store(data, user_id, user_ik)
        # check we can decrypt the data
        self.assertEquals(data, encrypted.get(user_id, user_ik))

if __name__ == '__main__':
    unittest.main()

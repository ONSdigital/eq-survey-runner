import unittest

from app.storage.encrypted_questionnaire_storage import EncryptedQuestionnaireStorage, generate_key


class TestEncryptedQuestionnaireStorage(unittest.TestCase):

    def test_encrypted_storage_requires_user_id(self):
        with self.assertRaises(ValueError):
            EncryptedQuestionnaireStorage(None, "key")

    def test_encrypted_storage_requires_user_ik(self):
        with self.assertRaises(ValueError):
            EncryptedQuestionnaireStorage("1", None)

    def test_generate_cek(self):
        cek1 = generate_key("user1", "user_ik_1")
        cek2 = generate_key("user1", "user_ik_1")
        cek3 = generate_key("user2", "user_ik_2")
        self.assertEqual(cek1, cek2)
        self.assertNotEqual(cek1, cek3)
        self.assertNotEqual(cek2, cek3)

    def test_generate_cek_different_user_ids(self):
        cek1 = generate_key("user1", "user_ik_1")
        cek2 = generate_key("user1", "user_ik_1")
        cek3 = generate_key("user2", "user_ik_1")
        self.assertEqual(cek1, cek2)
        self.assertNotEqual(cek1, cek3)
        self.assertNotEqual(cek2, cek3)

    def test_generate_cek_different_user_iks(self):
        cek1 = generate_key("user1", "user_ik_1")
        cek2 = generate_key("user1", "user_ik_1")
        cek3 = generate_key("user1", "user_ik_2")
        self.assertEqual(cek1, cek2)
        self.assertNotEqual(cek1, cek3)
        self.assertNotEqual(cek2, cek3)

    def test_generate_cek_different_pepper(self):
        cek1 = generate_key("user1", "user_ik_1")
        cek2 = generate_key("user1", "user_ik_1", "test")
        self.assertNotEqual(cek1, cek2)

    def test_store_and_get(self):
        user_id = '1'
        user_ik = '2'
        encrypted = EncryptedQuestionnaireStorage(user_id, user_ik)
        data = "test"
        encrypted.add_or_update(data)
        # check we can decrypt the data
        self.assertEqual("test", encrypted.get_user_data())

if __name__ == '__main__':
    unittest.main()

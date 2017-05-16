import unittest

from app import Database
from app.storage.encrypted_questionnaire_storage import EncryptedQuestionnaireStorage


# pylint: disable=W0212
class TestEncryptedQuestionnaireStorage(unittest.TestCase):

    def setUp(self):
        self.database = Database("sqlite://", 1, 0)
        self.storage = EncryptedQuestionnaireStorage(self.database, "user_id", "user_ik", "pepper")

    def test_encrypted_storage_requires_user_id(self):
        with self.assertRaises(ValueError):
            EncryptedQuestionnaireStorage(self.database, None, "key", "pepper")

    def test_encrypted_storage_requires_user_ik(self):
        with self.assertRaises(ValueError):
            EncryptedQuestionnaireStorage(self.database, "1", None, "pepper")

    def test_encrypted_storage_requires_pepper(self):
        with self.assertRaises(ValueError):
            EncryptedQuestionnaireStorage(self.database, "1", "key", None)

    def test_generate_cek(self):
        cek1 = EncryptedQuestionnaireStorage(self.database, "user1", "user_ik_1", "pepper")._cek
        cek2 = EncryptedQuestionnaireStorage(self.database, "user1", "user_ik_1", "pepper")._cek
        cek3 = EncryptedQuestionnaireStorage(self.database, "user2", "user_ik_2", "pepper")._cek
        self.assertEqual(cek1, cek2)
        self.assertNotEqual(cek1, cek3)
        self.assertNotEqual(cek2, cek3)

    def test_generate_cek_different_user_ids(self):
        cek1 = EncryptedQuestionnaireStorage(self.database, "user1", "user_ik_1", "pepper")._cek
        cek2 = EncryptedQuestionnaireStorage(self.database, "user1", "user_ik_1", "pepper")._cek
        cek3 = EncryptedQuestionnaireStorage(self.database, "user2", "user_ik_1", "pepper")._cek
        self.assertEqual(cek1, cek2)
        self.assertNotEqual(cek1, cek3)
        self.assertNotEqual(cek2, cek3)

    def test_generate_cek_different_user_iks(self):
        cek1 = EncryptedQuestionnaireStorage(self.database, "user1", "user_ik_1", "pepper")._cek
        cek2 = EncryptedQuestionnaireStorage(self.database, "user1", "user_ik_1", "pepper")._cek
        cek3 = EncryptedQuestionnaireStorage(self.database, "user1", "user_ik_2", "pepper")._cek
        self.assertEqual(cek1, cek2)
        self.assertNotEqual(cek1, cek3)
        self.assertNotEqual(cek2, cek3)

    def test_generate_cek_different_pepper(self):
        cek1 = EncryptedQuestionnaireStorage(self.database, "user1", "user_ik_1", "pepper")._cek
        cek2 = EncryptedQuestionnaireStorage(self.database, "user1", "user_ik_1", "test")._cek
        self.assertNotEqual(cek1, cek2)

    def test_store_and_get(self):
        user_id = '1'
        user_ik = '2'
        encrypted = EncryptedQuestionnaireStorage(self.database, user_id, user_ik, "pepper")
        data = "test"
        encrypted.add_or_update(data)
        # check we can decrypt the data
        self.assertEqual("test", encrypted.get_user_data())

    def test_store(self):
        data = 'test'
        self.assertIsNone(self.storage.add_or_update(data))
        self.assertIsNotNone(self.storage.get_user_data())  # pylint: disable=protected-access

    def test_get(self):
        data = 'test'
        self.storage.add_or_update(data)
        self.assertEqual(data, self.storage.get_user_data())

    def test_delete(self):
        data = 'test'
        self.storage.add_or_update(data)
        self.assertEqual(data, self.storage.get_user_data())
        self.storage.delete()
        self.assertIsNone(self.storage.get_user_data())  # pylint: disable=protected-access

if __name__ == '__main__':
    unittest.main()

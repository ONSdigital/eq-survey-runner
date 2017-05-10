import unittest

from mock import Mock, patch
from sqlalchemy.exc import IntegrityError

from app import settings
from app.storage.encrypted_questionnaire_storage import EncryptedQuestionnaireStorage


# pylint: disable=W0212
class TestEncryptedQuestionnaireStorage(unittest.TestCase):

    def setUp(self):
        settings.EQ_SERVER_SIDE_STORAGE_DATABASE_URL = "sqlite://"
        self.storage = EncryptedQuestionnaireStorage("user_id", "user_ik", "pepper")

    def test_encrypted_storage_requires_user_id(self):
        with self.assertRaises(ValueError):
            EncryptedQuestionnaireStorage(None, "key", "pepper")

    def test_encrypted_storage_requires_user_ik(self):
        with self.assertRaises(ValueError):
            EncryptedQuestionnaireStorage("1", None, "pepper")

    def test_encrypted_storage_requires_pepper(self):
        with self.assertRaises(ValueError):
            EncryptedQuestionnaireStorage("1", "key", None)

    def test_generate_cek(self):
        cek1 = EncryptedQuestionnaireStorage("user1", "user_ik_1", "pepper")._cek
        cek2 = EncryptedQuestionnaireStorage("user1", "user_ik_1", "pepper")._cek
        cek3 = EncryptedQuestionnaireStorage("user2", "user_ik_2", "pepper")._cek
        self.assertEqual(cek1, cek2)
        self.assertNotEqual(cek1, cek3)
        self.assertNotEqual(cek2, cek3)

    def test_generate_cek_different_user_ids(self):
        cek1 = EncryptedQuestionnaireStorage("user1", "user_ik_1", "pepper")._cek
        cek2 = EncryptedQuestionnaireStorage("user1", "user_ik_1", "pepper")._cek
        cek3 = EncryptedQuestionnaireStorage("user2", "user_ik_1", "pepper")._cek
        self.assertEqual(cek1, cek2)
        self.assertNotEqual(cek1, cek3)
        self.assertNotEqual(cek2, cek3)

    def test_generate_cek_different_user_iks(self):
        cek1 = EncryptedQuestionnaireStorage("user1", "user_ik_1", "pepper")._cek
        cek2 = EncryptedQuestionnaireStorage("user1", "user_ik_1", "pepper")._cek
        cek3 = EncryptedQuestionnaireStorage("user1", "user_ik_2", "pepper")._cek
        self.assertEqual(cek1, cek2)
        self.assertNotEqual(cek1, cek3)
        self.assertNotEqual(cek2, cek3)

    def test_generate_cek_different_pepper(self):
        cek1 = EncryptedQuestionnaireStorage("user1", "user_ik_1", "pepper")._cek
        cek2 = EncryptedQuestionnaireStorage("user1", "user_ik_1", "test")._cek
        self.assertNotEqual(cek1, cek2)

    def test_store_and_get(self):
        user_id = '1'
        user_ik = '2'
        encrypted = EncryptedQuestionnaireStorage(user_id, user_ik, "pepper")
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

    def test_store_rollback(self):
        # Given
        data = 'test'

        with patch('app.storage.encrypted_questionnaire_storage.db_session', autospec=True) as db_session:
            db_session.commit.side_effect = IntegrityError(Mock(), Mock(), Mock())

            # When
            try:
                self.storage.add_or_update(data)
            except IntegrityError:
                pass

            # Then
            db_session.rollback.assert_called_once_with()

    def test_delete_rollback(self):
        # Given
        data = 'test'
        self.storage.add_or_update(data)

        with patch('app.storage.encrypted_questionnaire_storage.db_session', autospec=True) as db_session:
            db_session.commit.side_effect = IntegrityError(Mock(), Mock(), Mock())

            # When
            try:
                self.storage.delete()
            except IntegrityError:
                pass

            # Then
            db_session.rollback.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()

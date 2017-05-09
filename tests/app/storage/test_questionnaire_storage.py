import unittest

from mock import Mock, patch
from sqlalchemy.exc import IntegrityError

from app import settings
from app.storage.encrypted_questionnaire_storage import EncryptedQuestionnaireStorage


class TestQuestionnaireStorage(unittest.TestCase):

    def setUp(self):
        settings.EQ_SERVER_SIDE_STORAGE_DATABASE_URL = "sqlite://"
        self.storage = EncryptedQuestionnaireStorage("user_id", "user_ik", "pepper")

    def test_store(self):
        data = 'test'
        self.assertIsNone(self.storage.add_or_update(data))
        self.assertIsNotNone(self.storage._find_questionnaire_state())  # pylint: disable=protected-access

    def test_get(self):
        data = 'test'
        self.storage.add_or_update(data)
        self.assertEqual(data, self.storage.get_user_data())

    def test_delete(self):
        data = 'test'
        self.storage.add_or_update(data)
        self.assertEqual(data, self.storage.get_user_data())
        self.storage.delete()
        self.assertIsNone(self.storage._find_questionnaire_state())  # pylint: disable=protected-access

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

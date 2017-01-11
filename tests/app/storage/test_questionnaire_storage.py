import unittest

from mock import Mock, patch
from sqlalchemy.exc import IntegrityError

from app import settings
from app.storage.questionnaire_storage import QuestionnaireStorage


class TestQuestionnaireStorage(unittest.TestCase):

    def setUp(self):
        settings.EQ_SERVER_SIDE_STORAGE_DATABASE_URL = "sqlite://"
        self.storage = QuestionnaireStorage("1")

    def test_store(self):
        data = {'test': 'test'}
        self.assertIsNone(self.storage.add_or_update(data))
        self.assertTrue(self.storage.exists())

    def test_get(self):
        data = {'test': 'test'}
        self.storage.add_or_update(data)
        self.assertEqual(data, self.storage.get_user_data())

    def test_delete(self):
        data = {'test': 'test'}
        self.storage.add_or_update(data)
        self.assertEqual(data, self.storage.get_user_data())
        self.storage.delete()
        self.assertFalse(self.storage.exists())

    def test_store_rollback(self):
        # Given
        data = {'test': 'test'}

        with patch('app.storage.questionnaire_storage.db_session', autospec=True) as db_session:
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
        data = {'test': 'test'}
        self.storage.add_or_update(data)

        with patch('app.storage.questionnaire_storage.db_session', autospec=True) as db_session:
            db_session.commit.side_effect = IntegrityError(Mock(), Mock(), Mock())

            # When
            try:
                self.storage.delete()
            except IntegrityError:
                pass

            # Then
            db_session.rollback.assert_called_once_with()

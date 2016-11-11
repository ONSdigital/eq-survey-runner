from mock import Mock, patch
from sqlalchemy.exc import IntegrityError

from app.storage.database_storage import DatabaseStorage
from app import settings
import unittest


class TestDatabaseStorage(unittest.TestCase):

    def setUp(self):
        settings.EQ_SERVER_SIDE_STORAGE_DATABASE_URL = "sqlite://"
        self.storage = DatabaseStorage()

    def tearDown(self):
        # always clear out the memory between test runs
        self.storage.clear()

    def test_store(self):
        data = {'test': 'test'}
        self.assertIsNone(self.storage.store(data, "1"))
        self.assertTrue(self.storage.has_data("1"))

    def test_get(self):
        data = {'test': 'test'}
        self.storage.store(data, "1")
        self.assertEqual(data, self.storage.get("1"))

    def test_delete(self):
        data = {'test': 'test'}
        self.storage.store(data, "1")
        self.assertEqual(data, self.storage.get("1"))
        self.storage.delete("1")
        self.assertFalse(self.storage.has_data("1"))
        self.assertIsNone(self.storage.get("1"))

    def test_clear(self):
        data = {'test': 'test'}
        self.storage.store(data, "1")
        self.assertEqual(data, self.storage.get("1"))
        self.storage.clear()
        self.assertFalse(self.storage.has_data("1"))
        self.assertIsNone(self.storage.get("1"))

    def test_store_rollback(self):
        # Given
        data = {'test': 'test'}

        with patch('app.storage.database_storage.db_session', autospec=True) as db_session:
            db_session.commit.side_effect = IntegrityError(Mock(), Mock(), Mock())

            # When
            try:
                self.storage.store(data, "1")
            except IntegrityError:
                pass

            # Then
            db_session.rollback.assert_called_once_with()

    def test_delete_rollback(self):
        # Given
        data = {'test': 'test'}
        self.storage.store(data, "1")

        with patch('app.storage.database_storage.db_session', autospec=True) as db_session:
            db_session.commit.side_effect = IntegrityError(Mock(), Mock(), Mock())

            # When
            try:
                self.storage.delete("1")
            except IntegrityError:
                pass

            # Then
            db_session.rollback.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()

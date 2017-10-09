import uuid
from unittest import TestCase


from mock import patch

from app.data_model.database import Database


class TestDatabaseSetupRetry(TestCase):

    def _test_database_retry(self, retry_count, exception):
        # Given a retry count of 'retry_count'
        # And 'exception' is always raised when trying to setup the database/connection
        with patch('time.sleep'), patch('app.data_model.database.Database._create_session_and_engine', autospec=True) as setup:
            setup.side_effect = exception

            # When I attempt to setup the database
            # Then a TimeoutError is raised
            with self.assertRaises(TimeoutError) as exception:
                Database(driver='sqlite',
                         database_name='',
                         setup_attempts=retry_count)

            # And the TimeoutError explains the failure
            self.assertIn('failed to setup database', exception.exception.args)

            # And the database setup was tried retry_count times
            self.assertEqual(setup.call_count, retry_count)

    def test_database_retry_exceptions(self):
        self._test_database_retry(0, ConnectionRefusedError)
        self._test_database_retry(5, ConnectionRefusedError)
        self._test_database_retry(10, ConnectionRefusedError)
        self._test_database_retry(3, Exception)
        self._test_database_retry(3, ValueError)

    def test_database_retry_success(self):
        # Given the database setup returns successfully first time
        # When I call the create
        database = Database(driver='sqlite',
                            database_name='',
                            setup_attempts=1,
                            setup_retry_delay=0)

        # pylint: disable=maybe-no-member
        # pylint: disable=protected-access
        # Then a value is successfully returned
        self.assertTrue(database._db_session.is_active)

    def test_database_retry_success_after_attempts(self):
        # Given the database setup fails twice then succeeds
        with patch('time.sleep'), patch('app.data_model.database.Database._create_session_and_engine', autospec=True) as setup:
            setup.side_effect = iter([ConnectionRefusedError, ConnectionRefusedError, 'success'])

            # When I call the create with retry function
            database = Database(driver='sqlite',
                                database_name='',
                                setup_attempts=3,
                                setup_retry_delay=0)

            # pylint: disable=protected-access
            # Then a value is successfully returned
            self.assertEqual(database._db_session, 'success')

            # And the setup was called three times before succeeding
            self.assertEqual(setup.call_count, 3)

    def test_database_url_creation_for_non_sqlite(self):
        # Given the database setup fails twice then succeeds
        with patch('app.data_model.database.Database._create_session_and_engine'):

            password = str(uuid.uuid4())

            # When I call the create with retry function
            database = Database(driver='postgresql',
                                host='localhost',
                                port=5432,
                                username='testUsername',
                                password=password,
                                database_name='digitaleqrds',
                                setup_attempts=1,
                                setup_retry_delay=0)

            # pylint: disable=protected-access
            # Then a value is successfully returned
            self.assertEqual(database._database_url, 'postgresql://testUsername:' + password + '@localhost:5432/digitaleqrds')

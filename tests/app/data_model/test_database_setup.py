from unittest import TestCase

from mock import patch

from app.data_model.database import _create_session_and_engine_with_retry
from app import settings


class TestDatabaseSetupRetry(TestCase):

    def _test_database_retry(self, retry_count, exception):
        # Given a retry count of 'retry_count'
        # And 'exception' is always raised when trying to setup the database/connection
        settings.EQ_SERVER_SIDE_STORAGE_DATABASE_SETUP_RETRY_COUNT = retry_count
        with patch('time.sleep'), patch('app.data_model.database._create_session_and_engine', autospec=True) as setup:
            setup.side_effect = exception

            # When I attempt to setup the database
            # Then a TimeoutError is raised
            with self.assertRaises(TimeoutError) as exception:
                _create_session_and_engine_with_retry()

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
        with patch('time.sleep'), patch('app.data_model.database._create_session_and_engine', autospec=True) as setup:
            setup.return_value = 'something'

            # When I call the create with retry function
            ret = _create_session_and_engine_with_retry()

            # Then a value is successfully returned
            self.assertEqual(ret, 'something')

            # And the setup was only attempted once
            setup.assert_called_once_with()

    def test_database_retry_success_after_attempts(self):
        # Given the database setup fails twice then succeeds
        with patch('time.sleep'), patch('app.data_model.database._create_session_and_engine', autospec=True) as setup:
            setup.side_effect = iter([ConnectionRefusedError, ConnectionRefusedError, 'success'])

            # When I call the create with retry function
            ret = _create_session_and_engine_with_retry()

            # Then a value is successfully returned
            self.assertEqual(ret, 'success')

            # And the setup was called three times before succeeding
            self.assertEqual(setup.call_count, 3)

from app.data_model.database import EQSession
from app.authentication.session_storage import SessionStorage, EQ_SESSION_ID

import flask
from mock import patch, Mock
from sqlalchemy.exc import IntegrityError

from tests.app.app_context_test_case import AppContextTestCase


# SQLAlchemy confuses pylint and we want to override a protected method here
# pylint: disable=no-member,protected-access


class TestSessionManager(AppContextTestCase):

    def setUp(self):
        super().setUp()
        self.session_storage = SessionStorage()

        # Create a patched db_session so we don't need a real database to test against
        self.db_session_patcher = patch('app.authentication.session_storage.db_session', autospec=True)
        self.addCleanup(self.db_session_patcher.stop)
        self.db_session = self.db_session_patcher.start()

        # Note each test will need to create a test_request_context
        # in order to access the Flask session object

    def test_store_new_user_id_then_replace(self):
        with self.test_request_context('/status'):
            # Store a user id for the first time
            self.session_storage.store_user_id('1')

            # When we store the user_id we generate a GUID and use that
            # as the session_id mapped to the user_id in the database
            self.assertTrue(EQ_SESSION_ID in flask.session)
            self.assertIsNotNone(flask.session[EQ_SESSION_ID])
            self.assertEqual(self.db_session.add.call_count, 1)

            # Store the GUID so we can check it changes
            eq_session_id = flask.session[EQ_SESSION_ID]

            # Try replacing the session with a new one
            self.session_storage.store_user_id('2')

            # Session GUID should have changed
            self.assertEqual(self.db_session.add.call_count, 2)
            self.assertNotEqual(eq_session_id, flask.session[EQ_SESSION_ID])

    def test_should_not_clear_with_no_session_data(self):
        with self.test_request_context('/status'):
            # Calling clear with no session should be safe to do
            self.session_storage.clear()

            # No database calls should have been made
            self.assertFalse(self.db_session.delete.called)

    def test_should_not_clear_with_no_session_in_database(self):
        with self.test_request_context('/status'):
            user_id = 'test_clear_user_id'

            # Store a user_id
            self.session_storage.store_user_id(user_id)

            # Mocking database session lookup, return None from database
            self.session_storage._get_user_session = lambda eq_session_id: None

            # Call clear with a valid user_id but no session in database
            self.session_storage.clear()

            # No database calls should have been made
            self.assertFalse(self.db_session.delete.called)

    def test_should_clear_with_session_and_data(self):
        with self.test_request_context('/status'):
            user_id = 'test_clear_user_id'

            # Store a user id
            self.session_storage.store_user_id(user_id)

            # Mocking database session lookup, to return a valid result
            eq_session = EQSession(flask.session[EQ_SESSION_ID], user_id)
            self.session_storage._get_user_session = lambda eq_session_id: eq_session

            # Call clear with a valid user_id and valid session in database
            self.session_storage.clear()

            # Should have attempted to remove it from the database
            self.assertEqual(self.db_session.delete.call_count, 1)
            self.db_session.delete.assert_called_once_with(eq_session)

    def test_store_user_id_rollback(self):
        with self.test_request_context('/status'):
            # Given
            self.db_session.commit.side_effect = IntegrityError(Mock(), Mock(), Mock())

            # When
            with self.assertRaises(IntegrityError):
                self.session_storage.store_user_id('3')

            # Then
            self.db_session.rollback.assert_called_once_with()

    def test_clear_rollback(self):
        with self.test_request_context('/status'):
            # Given
            user_id = '1'

            # Store the user_id to lookup later
            self.session_storage.store_user_id(user_id)

            # Mocking database session lookup, replace internal function on SessionStorage
            eq_session = EQSession('123', user_id)
            self.session_storage._get_user_session = lambda eq_session_id: eq_session

            self.db_session.commit.side_effect = IntegrityError(Mock(), Mock(), Mock())

            # When
            with self.assertRaises(IntegrityError):
                self.session_storage.clear()

            # Then
            self.db_session.rollback.assert_called_once_with()

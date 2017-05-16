from app.data_model.database import EQSession, Database
from app.authentication.session_storage import SessionStorage, EQ_SESSION_ID

import flask
from mock import Mock

from tests.app.app_context_test_case import AppContextTestCase


# SQLAlchemy confuses pylint and we want to override a protected method here
# pylint: disable=no-member,protected-access


class TestSessionManager(AppContextTestCase):

    def setUp(self):
        super().setUp()
        self.database = Mock(Database("sqlite://", 1, 0))
        self.session_storage = SessionStorage(self.database)

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
            self.assertEqual(self.database.add.call_count, 1)

            # Store the GUID so we can check it changes
            eq_session_id = flask.session[EQ_SESSION_ID]

            # Try replacing the session with a new one
            self.session_storage.store_user_id('2')

            # Session GUID should have changed
            self.assertEqual(self.database.add.call_count, 2)
            self.assertNotEqual(eq_session_id, flask.session[EQ_SESSION_ID])

    def test_should_not_clear_with_no_session_data(self):
        with self.test_request_context('/status'):
            # Calling clear with no session should be safe to do
            self.session_storage.delete_session_from_db()

            # No database calls should have been made
            self.assertFalse(self.database.delete.called)

    def test_should_not_clear_with_no_session_in_database(self):
        with self.test_request_context('/status'):
            user_id = 'test_clear_user_id'

            # Store a user_id
            self.session_storage.store_user_id(user_id)

            # Mocking database session lookup, return None from database
            self.session_storage._get_user_session = lambda eq_session_id: None

            # Call clear with a valid user_id but no session in database
            self.session_storage.delete_session_from_db()

            # No database calls should have been made
            self.assertFalse(self.database.delete.called)

    def test_should_clear_with_session_and_data(self):
        with self.test_request_context('/status'):
            user_id = 'test_clear_user_id'

            # Store a user id
            self.session_storage.store_user_id(user_id)

            # Mocking database session lookup, to return a valid result
            eq_session = EQSession(flask.session[EQ_SESSION_ID], user_id)
            self.session_storage._get_user_session = lambda eq_session_id: eq_session

            # Call clear with a valid user_id and valid session in database
            self.session_storage.delete_session_from_db()

            # Should have attempted to remove it from the database
            self.assertEqual(self.database.delete.call_count, 1)
            self.database.delete.assert_called_once_with(eq_session)

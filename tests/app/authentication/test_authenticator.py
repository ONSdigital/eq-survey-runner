from flask import session
from mock import patch

from app.data_model.session_data import SessionData
from app.settings import USER_IK
from app.authentication.authenticator import load_user, request_load_user, user_loader
from app.data_model.session_store import SessionStore
from tests.app.app_context_test_case import AppContextTestCase


class TestAuthenticator(AppContextTestCase): # pylint: disable=too-many-public-methods

    def setUp(self):
        super().setUp()
        self.session_data = SessionData(
            tx_id='tx_id',
            eq_id='eq_id',
            form_type='form_type',
            period_str='period_str',
            language_code=None,
            survey_url=None,
            ru_name='ru_name',
            ru_ref='ru_ref',
        )
        self.session_store = SessionStore('user_ik', 'pepper', 'eq_session_id')

    def test_check_session_with_user_id_in_session(self):
        with self.test_request_context('/status'):
            with patch('app.authentication.authenticator.get_session_store', return_value=self.session_store):
                # Given
                self.session_store.create('eq_session_id', 'user_id', self.session_data)
                session[USER_IK] = 'user_ik'

                # When
                user = load_user()

                # Then
                self.assertEqual(user.user_id, 'user_id')
                self.assertEqual(user.user_ik, 'user_ik')

    def test_check_session_with_no_user_id_in_session(self):
        with self.test_request_context('/status'):
            with patch('app.authentication.authenticator.get_session_store', return_value=None):
                # When
                user = load_user()

                # Then
                self.assertIsNone(user)

    def test_load_user(self):
        with self.test_request_context('/status'):
            with patch('app.authentication.authenticator.get_session_store', return_value=self.session_store):
                # Given
                self.session_store.create('eq_session_id', 'user_id', self.session_data)
                session[USER_IK] = 'user_ik'

                # When
                user = user_loader(None)

                # Then
                self.assertEqual(user.user_id, 'user_id')
                self.assertEqual(user.user_ik, 'user_ik')

    def test_request_load_user(self):
        with self.test_request_context('/status'):
            with patch('app.authentication.authenticator.get_session_store', return_value=self.session_store):
                # Given
                self.session_store.create('eq_session_id', 'user_id', self.session_data)
                session[USER_IK] = 'user_ik'

                # When
                user = request_load_user(None)

                # Then
                self.assertEqual(user.user_id, 'user_id')
                self.assertEqual(user.user_ik, 'user_ik')

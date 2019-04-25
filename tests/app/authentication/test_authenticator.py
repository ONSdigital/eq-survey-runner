from datetime import datetime, timedelta

from dateutil.tz import tzutc
from flask import session as cookie_session
from mock import patch

from app.authentication.authenticator import load_user, request_load_user, user_loader
from app.data_model.session_data import SessionData
from app.data_model.session_store import SessionStore
from app.settings import USER_IK
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
            case_id='case_id'
        )
        self.session_store = SessionStore('user_ik', 'pepper', 'eq_session_id')
        self.expires_at = datetime.now(tzutc()) + timedelta(seconds=5)

    def test_check_session_with_user_id_in_session(self):
        with self.app_request_context('/status'):
            with patch('app.authentication.authenticator.get_session_store', return_value=self.session_store):
                # Given
                self.session_store.create('eq_session_id', 'user_id', self.session_data, self.expires_at)
                cookie_session[USER_IK] = 'user_ik'

                # When
                user = load_user()

                # Then
                self.assertEqual(user.user_id, 'user_id')
                self.assertEqual(user.user_ik, 'user_ik')

    def test_check_session_with_no_user_id_in_session(self):
        with self.app_request_context('/status'):
            with patch('app.authentication.authenticator.get_session_store', return_value=None):
                # When
                user = load_user()

                # Then
                self.assertIsNone(user)

    def test_load_user(self):
        with self.app_request_context('/status'):
            with patch('app.authentication.authenticator.get_session_store', return_value=self.session_store):
                # Given
                self.session_store.create('eq_session_id', 'user_id', self.session_data, self.expires_at)
                cookie_session[USER_IK] = 'user_ik'

                # When
                user = user_loader(None)

                # Then
                self.assertEqual(user.user_id, 'user_id')
                self.assertEqual(user.user_ik, 'user_ik')

    def test_request_load_user(self):
        with self.app_request_context('/status'):
            with patch('app.authentication.authenticator.get_session_store', return_value=self.session_store):
                # Given
                self.session_store.create('eq_session_id', 'user_id', self.session_data, self.expires_at)
                cookie_session[USER_IK] = 'user_ik'

                # When
                user = request_load_user(None)

                # Then
                self.assertEqual(user.user_id, 'user_id')
                self.assertEqual(user.user_ik, 'user_ik')

    def test_no_user_when_session_has_expired(self):
        with self.app_request_context('/status'):
            with patch('app.authentication.authenticator.get_session_store', return_value=self.session_store):
                # Given
                self.session_store.create('eq_session_id', 'user_id', self.session_data, expires_at=datetime.now(tzutc()))
                cookie_session[USER_IK] = 'user_ik'

                # When
                user = user_loader(None)

                # Then
                self.assertIsNone(user)
                self.assertIsNone(cookie_session.get(USER_IK))

    def test_valid_user_does_not_extend_session_expiry_when_expiry_less_than_60_seconds_different(self):
        with self.app_request_context('/status'):
            with patch('app.authentication.authenticator.get_session_store', return_value=self.session_store):
                # Given
                self.session_store.create('eq_session_id', 'user_id', self.session_data, self.expires_at)
                cookie_session[USER_IK] = 'user_ik'
                cookie_session['expires_in'] = 5

                # When
                user = user_loader(None)

                # Then
                self.assertEqual(user.user_id, 'user_id')
                self.assertEqual(user.user_ik, 'user_ik')
                self.assertEqual(user.is_authenticated, True)
                self.assertEqual(self.session_store.expiration_time, self.expires_at)

    def test_valid_user_extends_session_expiry_when_expiry_greater_than_60_seconds_different(self):
        with self.app_request_context('/status'):
            with patch('app.authentication.authenticator.get_session_store', return_value=self.session_store):
                # Given
                self.session_store.create('eq_session_id', 'user_id', self.session_data, self.expires_at)
                cookie_session[USER_IK] = 'user_ik'
                cookie_session['expires_in'] = 600

                # When
                user = user_loader(None)

                # Then
                self.assertEqual(user.user_id, 'user_id')
                self.assertEqual(user.user_ik, 'user_ik')
                self.assertEqual(user.is_authenticated, True)
                self.assertGreater(self.session_store.expiration_time, self.expires_at)

    def test_session_still_valid_without_expiration_time(self):
        with self.app_request_context('/status'):
            with patch('app.authentication.authenticator.get_session_store', return_value=self.session_store):
                # Given
                self.session_store.create('eq_session_id', 'user_id', self.session_data)  # expires_at = None
                cookie_session[USER_IK] = 'user_ik'

                # When
                user = user_loader(None)

                # Then
                self.assertEqual(user.user_id, 'user_id')
                self.assertEqual(user.user_ik, 'user_ik')
                self.assertEqual(user.is_authenticated, True)
                self.assertIsNone(self.session_store.expiration_time)

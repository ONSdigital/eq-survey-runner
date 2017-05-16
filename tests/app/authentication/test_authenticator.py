import unittest
from datetime import timedelta

from flask import Flask
from mock import patch, Mock, MagicMock

from app import Database, SessionStorage
from app.authentication.authenticator import load_user, request_load_user, user_loader


class TestAuthenticator(unittest.TestCase):

    def setUp(self):
        application = Flask(__name__)
        application.config['TESTING'] = True
        application.secret_key = 'you will not guess'
        application.permanent_session_lifetime = timedelta(seconds=1)
        self.application = application
        # Use an in memory database
        self.database = Database("sqlite://", 1, 0)
        self.session_storage = Mock(SessionStorage(self.database))

        application.eq = {'session_storage': self.session_storage}

    def test_check_session_with_user_id_in_session(self):
        with self.application.test_request_context():
            with patch('app.authentication.authenticator.get_questionnaire_store', return_value=MagicMock()):
                # Given
                self.session_storage.get_user_id = Mock(return_value='user_id')
                self.session_storage.get_user_ik = Mock(return_value='user_ik')

                # When
                user = load_user()

                # Then
                self.assertEqual(user.user_id, 'user_id')
                self.assertEqual(user.user_ik, 'user_ik')

    def test_check_session_with_no_user_id_in_session(self):
        with self.application.test_request_context():
            # Given
            self.session_storage.get_user_id = Mock(return_value=None)

            # When
            user = load_user()

            # Then
            self.assertIsNone(user)

    def test_load_user(self):
        with self.application.test_request_context():
            with patch('app.authentication.authenticator.get_questionnaire_store', return_value=MagicMock()):
                # Given
                self.session_storage.get_user_id = Mock(return_value='user_id')
                self.session_storage.get_user_ik = Mock(return_value='user_ik')

                # When
                user = user_loader(None)

                # Then
                self.assertEqual(user.user_id, 'user_id')
                self.assertEqual(user.user_ik, 'user_ik')

    def test_request_load_user(self):
        with self.application.test_request_context():
            with patch('app.authentication.authenticator.get_questionnaire_store', return_value=MagicMock()):
                # Given
                self.session_storage.get_user_id = Mock(return_value='user_id')
                self.session_storage.get_user_ik = Mock(return_value='user_ik')

                # When
                user = request_load_user(None)

                # Then
                self.assertEqual(user.user_id, 'user_id')
                self.assertEqual(user.user_ik, 'user_ik')

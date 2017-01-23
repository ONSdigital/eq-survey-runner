import unittest

from mock import patch, Mock, MagicMock

from app.authentication.authenticator import Authenticator, load_user, request_load_user


class TestAuthenticator(unittest.TestCase):

    def test_check_session_with_user_id_in_session(self):
        with patch('app.authentication.authenticator.session_storage') as session_storage, \
             patch('app.authentication.authenticator.get_questionnaire_store', return_value=MagicMock()):
            # Given
            session_storage.has_user_id = Mock(return_value=True)
            session_storage.get_user_id = Mock(return_value='user_id')
            session_storage.get_user_ik = Mock(return_value='user_ik')

            # When
            user = Authenticator().check_session()

            # Then
            self.assertEqual(user.user_id, 'user_id')
            self.assertEqual(user.user_ik, 'user_ik')

    def test_check_session_with_no_user_id_in_session(self):
        with patch('app.authentication.authenticator.session_storage') as session_storage:
            # Given
            session_storage.has_user_id = Mock(return_value=False)

            # When
            user = Authenticator().check_session()

            # Then
            self.assertIsNone(user)

    def test_load_user(self):
        with patch('app.authentication.authenticator.session_storage') as session_storage, \
             patch('app.authentication.authenticator.get_questionnaire_store', return_value=MagicMock()):
            # Given
            session_storage.has_user_id = Mock(return_value=True)
            session_storage.get_user_id = Mock(return_value='user_id')
            session_storage.get_user_ik = Mock(return_value='user_ik')

            # When
            user = load_user(None)

            # Then
            self.assertEqual(user.user_id, 'user_id')
            self.assertEqual(user.user_ik, 'user_ik')

    def test_request_load_user(self):
        with patch('app.authentication.authenticator.session_storage') as session_storage, \
             patch('app.authentication.authenticator.get_questionnaire_store', return_value=MagicMock()):
            # Given
            session_storage.has_user_id = Mock(return_value=True)
            session_storage.get_user_id = Mock(return_value='user_id')
            session_storage.get_user_ik = Mock(return_value='user_ik')

            # When
            user = request_load_user(None)

            # Then
            self.assertEqual(user.user_id, 'user_id')
            self.assertEqual(user.user_ik, 'user_ik')

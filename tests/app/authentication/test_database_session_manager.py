import unittest

from mock import patch, Mock
from sqlalchemy.exc import IntegrityError

from app.authentication.session_storage import SessionStorage, EQ_SESSION_ID


class TestSessionManager(unittest.TestCase):

    @staticmethod
    def test_store_user_id_rollback():
        # Given
        session_storage = SessionStorage()
        user_id = "1"

        with patch('app.authentication.session_storage.session'), \
                patch('app.authentication.session_storage.db_session', autospec=True) as db_session:
            db_session.commit.side_effect = IntegrityError(Mock(), Mock(), Mock())

            # When
            try:
                session_storage.store_user_id(user_id)
            except IntegrityError:
                pass

            # Then
            db_session.rollback.assert_called_once_with()

    @staticmethod
    def test_clear_rollback():
        # Given
        session_storage = SessionStorage()

        with patch('app.authentication.session_storage.session') as flask_session, \
                patch('app.authentication.session_storage.db_session', autospec=True) as db_session:
            # Mocking flask session dict lookup
            flask_session.__contains__ = Mock(return_value=True)
            flask_session.__getitem__ = Mock(side_effect={EQ_SESSION_ID, '1'})
            db_session.commit.side_effect = IntegrityError(Mock(), Mock(), Mock())

            # When
            try:
                session_storage.clear()
            except IntegrityError:
                pass

            # Then
            db_session.rollback.assert_called_once_with()

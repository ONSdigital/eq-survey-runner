from unittest import TestCase

from mock import patch, call, Mock
from sqlalchemy.exc import IntegrityError

from app.data_model.database import commit_or_rollback


class TestCommitOrRollback(TestCase):

    @staticmethod
    def test_commit_after_inserts():
        # Given
        with patch('app.data_model.database.db_session', autospec=True) as db_session:

            # When db_session action within commit_or_rollback
            with commit_or_rollback(db_session):
                db_session.add('data')

            # Then .add() followed by .commit()
            db_session.assert_has_calls([call.add('data'), call.commit()])

    @staticmethod
    def test_rollback_after_commit_fail():
        # Given
        with patch('app.data_model.database.db_session', autospec=True) as db_session:
            db_session.commit.side_effect = IntegrityError(Mock(), Mock(), Mock())

            try:
                # When db_session action within commit_or_rollback
                with commit_or_rollback(db_session):
                    pass
            except IntegrityError:
                pass

            # Then .add() followed by .rollback()
            db_session.assert_has_calls([call.commit(), call.rollback()])

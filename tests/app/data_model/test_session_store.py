from datetime import timedelta, datetime
from mock import patch

from app.data_model.session_store import SessionStore
from app.data_model.session_data import SessionData
from tests.app.app_context_test_case import AppContextTestCase


class SessionStoreTest(AppContextTestCase):
    def setUp(self):
        super().setUp()
        self._app.permanent_session_lifetime = timedelta(seconds=1)
        self.session_store = SessionStore()
        self.session_data = SessionData(
            tx_id='tx_id',
            eq_id='eq_id',
            form_type='form_type',
            period_str='period_str'
        )

    def test_no_session(self):
        with self._app.test_request_context():
            self.assertIsNone(self.session_store.user_id)
            self.assertIsNone(self.session_store.session_data)

    def test_create(self):
        with self._app.test_request_context():
            self.session_store.create('eq_session_id', 'test', self.session_data)
            self.assertEqual('eq_session_id', self.session_store.eq_session_id)
            self.assertEqual('test', self.session_store.user_id)
            self.assertEqual(self.session_data, self.session_store.session_data)

    def test_save(self):
        with self._app.test_request_context():
            self.session_store.create('eq_session_id', 'test', self.session_data).save()
            session_store = SessionStore('eq_session_id')
            self.assertEqual(session_store.session_data.tx_id, 'tx_id')

    def test_delete(self):
        with self._app.test_request_context():
            self.session_store.create('eq_session_id', 'test', self.session_data).save()
            self.assertEqual('test', self.session_store.user_id)
            self.session_store.delete()
            self.assertEqual(self.session_store.user_id, None)

    def test_add_data_to_session(self):
        with self._app.test_request_context():
            self.session_store.create('eq_session_id', 'test', self.session_data).save()
            current_time = datetime.utcnow().isoformat()
            self.session_store.session_data.submitted_time = current_time
            self.session_store.save()

            session_store = SessionStore('eq_session_id')
            self.assertEqual(session_store.session_data.submitted_time, current_time)

    def test_should_not_delete_when_no_session(self):
        with self.test_request_context('/status'):
            with patch('app.data_model.models.db.session.delete') as delete:

                # Call clear with a valid user_id but no session in database
                self.session_store.delete()

                # No database calls should have been made
                self.assertFalse(delete.called)

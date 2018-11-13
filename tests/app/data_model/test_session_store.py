import json
from datetime import datetime, timedelta

from jwcrypto import jwe
from jwcrypto.common import base64url_encode
from mock import patch
from tests.app.app_context_test_case import AppContextTestCase

from app.data_model.app_models import EQSession
from app.data_model.session_data import SessionData
from app.data_model.session_store import SessionStore
from app.storage import data_access, storage_encryption


class SessionStoreTest(AppContextTestCase):
    def setUp(self):
        super().setUp()
        self._app.permanent_session_lifetime = timedelta(seconds=1)
        self.session_store = SessionStore('user_ik', 'pepper')
        self.expires_at = datetime.utcnow() + timedelta(seconds=1)
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

    def test_no_session(self):
        with self._app.test_request_context():
            self.assertIsNone(self.session_store.user_id)
            self.assertIsNone(self.session_store.session_data)

    def test_create(self):
        with self._app.test_request_context():
            self.session_store.create('eq_session_id', 'test', self.session_data, self.expires_at)
            self.assertEqual('eq_session_id', self.session_store.eq_session_id)
            self.assertEqual('test', self.session_store.user_id)
            self.assertEqual(self.session_data, self.session_store.session_data)

    def test_save(self):
        with self._app.test_request_context():
            self.session_store.create('eq_session_id', 'test', self.session_data, self.expires_at).save()
            session_store = SessionStore('user_ik', 'pepper', 'eq_session_id')
            self.assertEqual(session_store.session_data.tx_id, 'tx_id')

    def test_delete(self):
        with self._app.test_request_context():
            self.session_store.create('eq_session_id', 'test', self.session_data, self.expires_at).save()
            self.assertEqual('test', self.session_store.user_id)
            self.session_store.delete()
            self.assertEqual(self.session_store.user_id, None)

    def test_create_save_delete_with_no_expiry(self):
        with self._app.test_request_context():
            self.session_store.create('eq_session_id', 'test', self.session_data).save()
            self.assertEqual('eq_session_id', self.session_store.eq_session_id)
            self.assertEqual('test', self.session_store.user_id)
            self.assertEqual(self.session_data, self.session_store.session_data)
            self.assertIsNone(self.session_store.expiration_time)

            self.session_store.delete()
            self.assertEqual(self.session_store.user_id, None)

    def test_add_data_to_session(self):
        with self._app.test_request_context():
            self.session_store.create('eq_session_id', 'test', self.session_data, self.expires_at).save()
            current_time = datetime.utcnow().isoformat()
            self.session_store.session_data.submitted_time = current_time
            self.session_store.save()

            session_store = SessionStore('user_ik', 'pepper', 'eq_session_id')
            self.assertEqual(session_store.session_data.submitted_time, current_time)

    def test_should_not_delete_when_no_session(self):
        with self.app_request_context('/status'):
            with patch('app.data_model.models.db.session.delete') as delete:

                # Call clear with a valid user_id but no session in database
                self.session_store.delete()

                # No database calls should have been made
                self.assertFalse(delete.called)

    def test_session_store_ignores_new_values_in_session_data(self):
        session_data = SessionData(
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

        session_data.additional_value = 'some cool new value you do not know about yet'

        with self._app.test_request_context():
            self.session_store.create('eq_session_id', 'test', session_data, self.expires_at).save()

            session_store = SessionStore('user_ik', 'pepper', 'eq_session_id')

            self.assertFalse(hasattr(session_store.session_data, 'additional_value'))

    def test_session_store_ignores_multiple_new_values_in_session_data(self):
        session_data = SessionData(
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

        session_data.additional_value = 'some cool new value you do not know about yet'
        session_data.second_additional_value = 'some other not so cool value'

        with self._app.test_request_context():
            self.session_store.create('eq_session_id', 'test', session_data, self.expires_at).save()

            session_store = SessionStore('user_ik', 'pepper', 'eq_session_id')

            self.assertFalse(hasattr(session_store.session_data, 'additional_value'))
            self.assertFalse(hasattr(session_store.session_data, 'second_additional_value'))

    def test_session_store_stores_trading_as_value_if_present(self):
        session_data = SessionData(
            tx_id='tx_id',
            eq_id='eq_id',
            form_type='form_type',
            period_str='period_str',
            language_code=None,
            survey_url=None,
            ru_name='ru_name',
            ru_ref='ru_ref',
            trad_as='trading_as',
            case_id='case_id'
        )
        with self._app.test_request_context():
            self.session_store.create('eq_session_id', 'test', session_data, self.expires_at).save()

            session_store = SessionStore('user_ik', 'pepper', 'eq_session_id')

            self.assertTrue(hasattr(session_store.session_data, 'trad_as'))

    def test_session_store_stores_none_for_trading_as_if_not_present(self):
        session_data = SessionData(
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
        with self._app.test_request_context():
            self.session_store.create('eq_session_id', 'test', session_data, self.expires_at).save()

            session_store = SessionStore('user_ik', 'pepper', 'eq_session_id')

            self.assertIsNone(session_store.session_data.trad_as)

    def test_session_store_reads_data_saved_without_trading_as_but_read_expecting_trading_as(self):
        old_session_data = SessionData(
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
        delattr(old_session_data, 'trad_as')   # Make class look like old style class
        with self._app.test_request_context():
            self.session_store.create('eq_session_id', 'test', old_session_data, self.expires_at).save()

            session_store = SessionStore('user_ik', 'pepper', 'eq_session_id')

            self.assertIsNone(session_store.session_data.trad_as)

    def test_session_store_reads_data_saved_with_trading_as_but_read_not_expecting_trading_as(self):
        """This test simulates the case where a session is created using a new session store that holds trading as
            but this gets read in an old session that does NOT support trading as """

        original_loads_func = json.loads

        class OldSessionData:
            """class representing what old sessions expect ( no trading as) """
            def __init__(self,
                         tx_id,
                         eq_id,
                         form_type,
                         period_str,
                         language_code,
                         survey_url,
                         ru_name,
                         ru_ref,
                         case_id,
                         case_ref=None,
                         account_service_url=None,
                         submitted_time=None,
                         **_):
                self.tx_id = tx_id
                self.eq_id = eq_id
                self.form_type = form_type
                self.period_str = period_str
                self.language_code = language_code
                self.survey_url = survey_url
                self.ru_name = ru_name
                self.ru_ref = ru_ref
                self.submitted_time = submitted_time
                self.case_id = case_id
                self.case_ref = case_ref
                self.account_service_url = account_service_url

        def old_json_loader(raw, object_hook):  # pylint: disable=unused-argument
            """replacement for json.loads to decode to old format ( no trading as) """

            old_data = original_loads_func(raw, object_hook=lambda d: OldSessionData(**d))   # call json.loads ,hook pointing to an old class
            return old_data

        session_data = SessionData(
            tx_id='tx_id',
            eq_id='eq_id',
            form_type='form_type',
            period_str='period_str',
            language_code=None,
            survey_url=None,
            ru_name='ru_name',
            ru_ref='ru_ref',
            trad_as='trading_as_name',
            case_id='case_id'
        )
        with self._app.test_request_context():

            with patch('app.data_model.session_store.json.loads', old_json_loader):  # patch json.loads to use old_json_loader above
                self.session_store.create('eq_session_id', 'test', session_data, self.expires_at).save()

                session_store = SessionStore('user_ik', 'pepper', 'eq_session_id')

                self.assertFalse(hasattr(session_store.session_data, 'trad_as'))


class TestLegacySessionStore(AppContextTestCase):
    """Session data used to be base64-encoded. For performance reasons the base64 encoding was removed.
    """
    def setUp(self):
        super().setUp()
        self.user_id = 'user_id'
        self.user_ik = 'user_ik'
        self.pepper = 'pepper'
        self.session_id = 'session_id'
        self.session_data = SessionData(
            tx_id='tx_id',
            eq_id='eq_id',
            form_type='form_type',
            period_str='period_str',
            language_code=None,
            survey_url=None,
            ru_name='ru_name',
            ru_ref='ru_ref',
            trad_as='trading_as_name',
            case_id='case_id'
        )

        # pylint: disable=protected-access
        self.key = storage_encryption.StorageEncryption._generate_key(
            self.user_id, self.user_ik, self.pepper)
        self._save_legacy_state_data(self.session_id, self.user_id, self.session_data)

    def test_load(self):
        session_store = SessionStore(self.user_ik, self.pepper, self.session_id)
        self.assertEqual(session_store.session_data.tx_id, self.session_data.tx_id)

    def _save_legacy_state_data(self, session_id, user_id, data):
        raw_data = json.dumps(vars(data))
        protected_header = {
            'alg': 'dir',
            'enc': 'A256GCM',
            'kid': '1,1',
        }

        jwe_token = jwe.JWE(
            plaintext=base64url_encode(raw_data),
            protected=protected_header,
            recipient=self.key
        )

        session_model = EQSession(
            session_id,
            user_id,
            jwe_token.serialize(compact=True)
        )
        data_access.put(session_model)

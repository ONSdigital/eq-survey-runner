import json
from datetime import datetime, timedelta

from flask import current_app
from jwcrypto import jwe
from jwcrypto.common import base64url_encode
from tests.app.app_context_test_case import AppContextTestCase

from app.data_model.app_models import EQSession
from app.data_model.session_data import SessionData
from app.data_model.session_store import SessionStore
from app.storage import storage_encryption


class SessionStoreTest(AppContextTestCase):
    def setUp(self):
        super().setUp()
        self._app.permanent_session_lifetime = timedelta(seconds=1)
        self.session_store = SessionStore('user_ik', 'pepper')
        self.expires_at = datetime.utcnow() + timedelta(seconds=1)
        self.session_data = SessionData(
            tx_id='tx_id',
            schema_name='some_schema_name',
            period_str='period_str',
            language_code=None,
            survey_url=None,
            ru_name='ru_name',
            ru_ref='ru_ref',
            questionnaire_id='questionnaire_id',
            response_id='response_id',
            case_id='case_id',
        )

    def test_no_session(self):
        with self._app.test_request_context():
            self.assertIsNone(self.session_store.user_id)
            self.assertIsNone(self.session_store.session_data)

    def test_create(self):
        with self._app.test_request_context():
            self.session_store.create(
                'eq_session_id', 'test', self.session_data, self.expires_at
            )
            self.assertEqual('eq_session_id', self.session_store.eq_session_id)
            self.assertEqual('test', self.session_store.user_id)
            self.assertEqual(self.session_data, self.session_store.session_data)

    def test_save(self):
        with self._app.test_request_context():
            self.session_store.create(
                'eq_session_id', 'test', self.session_data, self.expires_at
            ).save()
            session_store = SessionStore('user_ik', 'pepper', 'eq_session_id')
            self.assertEqual(session_store.session_data.tx_id, 'tx_id')

    def test_delete(self):
        with self._app.test_request_context():
            self.session_store.create(
                'eq_session_id', 'test', self.session_data, self.expires_at
            ).save()
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
            self.session_store.create(
                'eq_session_id', 'test', self.session_data, self.expires_at
            ).save()
            current_time = datetime.utcnow().isoformat()
            self.session_store.session_data.submitted_time = current_time
            self.session_store.save()

            session_store = SessionStore('user_ik', 'pepper', 'eq_session_id')
            self.assertEqual(session_store.session_data.submitted_time, current_time)

    def test_should_not_delete_when_no_session(self):
        with self.app_request_context('/status') as context:

            # Call clear with a valid user_id but no session in database
            self.session_store.delete()

            # No database calls should have been made
            self.assertEqual(context.app.eq['storage'].client.delete_call_count, 0)

    def test_session_store_ignores_new_values_in_session_data(self):
        session_data = SessionData(
            tx_id='tx_id',
            schema_name='some_schema_name',
            period_str='period_str',
            language_code=None,
            survey_url=None,
            ru_name='ru_name',
            ru_ref='ru_ref',
            response_id='response_id',
            questionnaire_id='questionnaire_id',
            case_id='case_id',
        )

        session_data.additional_value = 'some cool new value you do not know about yet'

        with self._app.test_request_context():
            self.session_store.create(
                'eq_session_id', 'test', session_data, self.expires_at
            ).save()

            session_store = SessionStore('user_ik', 'pepper', 'eq_session_id')

            self.assertFalse(hasattr(session_store.session_data, 'additional_value'))

    def test_session_store_ignores_multiple_new_values_in_session_data(self):
        session_data = SessionData(
            tx_id='tx_id',
            schema_name='some_schema_name',
            period_str='period_str',
            language_code=None,
            survey_url=None,
            ru_name='ru_name',
            ru_ref='ru_ref',
            response_id='response_id',
            questionnaire_id='questionnaire_id',
            case_id='case_id',
        )

        session_data.additional_value = 'some cool new value you do not know about yet'
        session_data.second_additional_value = 'some other not so cool value'

        with self._app.test_request_context():
            self.session_store.create(
                'eq_session_id', 'test', session_data, self.expires_at
            ).save()

            session_store = SessionStore('user_ik', 'pepper', 'eq_session_id')

            self.assertFalse(hasattr(session_store.session_data, 'additional_value'))
            self.assertFalse(
                hasattr(session_store.session_data, 'second_additional_value')
            )

    def test_session_store_stores_trading_as_value_if_present(self):
        session_data = SessionData(
            tx_id='tx_id',
            schema_name='some_schema_name',
            period_str='period_str',
            language_code=None,
            survey_url=None,
            ru_name='ru_name',
            ru_ref='ru_ref',
            response_id='response_id',
            questionnaire_id='questionnaire_id',
            trad_as='trading_as',
            case_id='case_id',
        )
        with self._app.test_request_context():
            self.session_store.create(
                'eq_session_id', 'test', session_data, self.expires_at
            ).save()

            session_store = SessionStore('user_ik', 'pepper', 'eq_session_id')

            self.assertTrue(hasattr(session_store.session_data, 'trad_as'))

    def test_session_store_stores_none_for_trading_as_if_not_present(self):
        session_data = SessionData(
            tx_id='tx_id',
            schema_name='some_schema_name',
            period_str='period_str',
            language_code=None,
            survey_url=None,
            ru_name='ru_name',
            ru_ref='ru_ref',
            response_id='response_id',
            questionnaire_id='questionnaire_id',
            case_id='case_id',
        )
        with self._app.test_request_context():
            self.session_store.create(
                'eq_session_id', 'test', session_data, self.expires_at
            ).save()

            session_store = SessionStore('user_ik', 'pepper', 'eq_session_id')

            self.assertIsNone(session_store.session_data.trad_as)


class TestSessionStoreEncoding(AppContextTestCase):
    """Session data used to be base64-encoded. For performance reasons the
    base64 encoding was removed.
    """

    def setUp(self):
        super().setUp()
        self.user_id = 'user_id'
        self.user_ik = 'user_ik'
        self.pepper = 'pepper'
        self.session_id = 'session_id'
        self.session_data = SessionData(
            tx_id='tx_id',
            schema_name='some_schema_name',
            period_str='period_str',
            language_code=None,
            survey_url=None,
            ru_name='ru_name',
            response_id='response_id',
            questionnaire_id='questionnaire_id',
            ru_ref='ru_ref',
            trad_as='trading_as_name',
            case_id='case_id',
        )

        # pylint: disable=protected-access
        self.key = storage_encryption.StorageEncryption._generate_key(
            self.user_id, self.user_ik, self.pepper
        )

    def test_legacy_load(self):
        self._save_session(
            self.session_id, self.user_id, self.session_data, legacy=True
        )
        session_store = SessionStore(self.user_ik, self.pepper, self.session_id)
        self.assertEqual(session_store.session_data.tx_id, self.session_data.tx_id)

    def test_load(self):
        self._save_session(self.session_id, self.user_id, self.session_data)
        session_store = SessionStore(self.user_ik, self.pepper, self.session_id)
        self.assertEqual(session_store.session_data.tx_id, self.session_data.tx_id)

    def _save_session(self, session_id, user_id, data, legacy=False):
        raw_data = json.dumps(vars(data))
        protected_header = {'alg': 'dir', 'enc': 'A256GCM', 'kid': '1,1'}

        if legacy:
            plaintext = base64url_encode(raw_data)
        else:
            plaintext = raw_data

        jwe_token = jwe.JWE(
            plaintext=plaintext, protected=protected_header, recipient=self.key
        )

        session_model = EQSession(
            session_id, user_id, jwe_token.serialize(compact=True)
        )
        current_app.eq['storage'].put(session_model)

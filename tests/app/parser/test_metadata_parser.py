import unittest
import uuid

from sdc.crypto.exceptions import InvalidTokenException
from app.storage.metadata_parser import parse_metadata, is_valid_metadata
from tests.app.framework.survey_runner_test_case import SurveyRunnerTestCase


class TestMetadataParser(SurveyRunnerTestCase):  # pylint: disable=too-many-public-methods

    def setUp(self):
        super().setUp()
        self.jwt = {
            'jti': str(uuid.uuid4()),
            'user_id': '1',
            'form_type': 'a',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '2',
            'period_id': '3',
            'period_str': '2016-01-01',
            'ref_p_start_date': '2016-02-02',
            'ref_p_end_date': '2016-03-03',
            'ru_ref': '2016-04-04',
            'ru_name': 'Apple',
            'return_by': '2016-07-07',
            'tx_id': '4ec3aa9e-e8ac-4c8d-9793-6ed88b957c2f',
            'case_id': '1234567890',
            'case_ref': '1000000000000001',
            'account_service_url': 'https://ras.ons.gov.uk'
        }
        with self.application.test_request_context():
            self.metadata = self.metadata = parse_metadata(self.jwt, {})

    def test_transaction_id(self):
        with self.application.test_request_context():
            self.assertEqual(self.jwt.get('tx_id'), self.metadata['tx_id'])

    def test_form_type(self):
        with self.application.test_request_context():
            self.assertEqual(self.jwt.get('form_type'), self.metadata['form_type'])

    def test_collection_id(self):
        with self.application.test_request_context():
            self.assertEqual(self.jwt.get('collection_exercise_sid'), self.metadata['collection_exercise_sid'])

    def test_get_eq_id(self):
        with self.application.test_request_context():
            self.assertEqual(self.jwt.get('eq_id'), self.metadata['eq_id'])

    def test_get_period_id(self):
        with self.application.test_request_context():
            self.assertEqual(self.jwt.get('period_id'), self.metadata['period_id'])

    def test_get_period_str(self):
        with self.application.test_request_context():
            self.assertEqual(self.jwt.get('period_str'), self.metadata['period_str'])

    def test_ref_p_start_date(self):
        with self.application.test_request_context():
            self.assertEqual(self.jwt.get('ref_p_start_date'), self.metadata['ref_p_start_date'])

    def test_ref_p_end_date(self):
        with self.application.test_request_context():
            self.assertEqual(self.jwt.get('ref_p_end_date'), self.metadata['ref_p_end_date'])

    def test_ru_ref(self):
        with self.application.test_request_context():
            self.assertEqual(self.jwt.get('ref_p_end_date'), self.metadata['ref_p_end_date'])

    def test_case_id(self):
        with self.application.test_request_context():
            self.assertEqual(self.jwt.get('case_id'), self.metadata['case_id'])

    def test_case_ref(self):
        with self.application.test_request_context():
            self.assertEqual(self.jwt.get('case_ref'), self.metadata['case_ref'])

    def test_account_service_url(self):
        with self.application.test_request_context():
            self.assertEqual(self.jwt.get('account_service_url'), self.metadata['account_service_url'])

    def test_is_valid(self):
        with self.application.test_request_context():
            self.assertTrue(is_valid_metadata(self.jwt, {}))

    def test_is_valid_fails_missing_user_id(self):
        jwt = {
            'jti': str(uuid.uuid4()),
            'form_type': 'a',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '2',
            'period_id': '3',
            'period_str': '2016-01-01',
            'ref_p_start_date': '2016-02-02',
            'ref_p_end_date': '2016-03-03',
            'ru_ref': '2016-04-04',
            'ru_name': 'Apple',
            'return_by': '2016-07-07'
        }
        valid, field = is_valid_metadata(jwt, {})
        self.assertFalse(valid)
        self.assertEqual('user_id', field)

    def test_is_valid_fails_missing_form_type(self):
        jwt = {
            'jti': str(uuid.uuid4()),
            'user_id': '1',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '2',
            'period_id': '3',
            'period_str': '2016-01-01',
            'ref_p_start_date': '2016-02-02',
            'ref_p_end_date': '2016-03-03',
            'ru_ref': '2016-04-04',
            'ru_name': 'Apple',
            'return_by': '2016-07-07'
        }
        valid, field = is_valid_metadata(jwt, {})
        self.assertFalse(valid)
        self.assertEqual('form_type', field)

    def test_is_valid_fails_missing_collection_exercise_sid(self):
        jwt = {
            'jti': str(uuid.uuid4()),
            'user_id': '1',
            'form_type': 'a',
            'eq_id': '2',
            'period_id': '3',
            'period_str': '2016-01-01',
            'ref_p_start_date': '2016-02-02',
            'ref_p_end_date': '2016-03-03',
            'ru_ref': '2016-04-04',
            'ru_name': 'Apple',
            'return_by': '2016-07-07'
        }
        valid, field = is_valid_metadata(jwt, {})
        self.assertFalse(valid)
        self.assertEqual('collection_exercise_sid', field)

    def test_is_valid_fails_missing_eq_id(self):
        jwt = {
            'jti': str(uuid.uuid4()),
            'user_id': '1',
            'form_type': 'a',
            'collection_exercise_sid': 'test-sid',
            'period_id': '3',
            'period_str': '2016-01-01',
            'ref_p_start_date': '2016-02-02',
            'ref_p_end_date': '2016-03-03',
            'ru_ref': '2016-04-04',
            'ru_name': 'Apple',
            'return_by': '2016-07-07'
        }
        valid, field = is_valid_metadata(jwt, {})
        self.assertFalse(valid)
        self.assertEqual('eq_id', field)

    def test_is_valid_fails_missing_period_id(self):
        jwt = {
            'jti': str(uuid.uuid4()),
            'user_id': '1',
            'form_type': 'a',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '2',
            'period_str': '2016-01-01',
            'ref_p_start_date': '2016-02-02',
            'ref_p_end_date': '2016-03-03',
            'ru_ref': '2016-04-04',
            'ru_name': 'Apple',
            'return_by': '2016-07-07'
        }
        valid, field = is_valid_metadata(jwt, {})
        self.assertFalse(valid)
        self.assertEqual('period_id', field)

    def test_is_valid_fails_missing_period_str(self):
        jwt = {
            'jti': str(uuid.uuid4()),
            'user_id': '1',
            'form_type': 'a',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '2',
            'period_id': '3',
            'ref_p_start_date': '2016-02-02',
            'ref_p_end_date': '2016-03-03',
            'ru_ref': '2016-04-04',
            'ru_name': 'Apple',
            'return_by': '2016-07-07'
        }
        valid, field = is_valid_metadata(jwt, {})
        self.assertFalse(valid)
        self.assertEqual('period_str', field)

    def test_is_valid_fails_missing_ref_p_start_date(self):
        jwt = {
            'jti': str(uuid.uuid4()),
            'user_id': '1',
            'form_type': 'a',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '2',
            'period_id': '3',
            'period_str': '2016-01-01',
            'ref_p_end_date': '2016-03-03',
            'ru_ref': '2016-04-04',
            'ru_name': 'Apple',
            'return_by': '2016-07-07'
        }
        valid, field = is_valid_metadata(jwt, {})
        self.assertFalse(valid)
        self.assertEqual('ref_p_start_date', field)

    def test_is_valid_fails_invalid_ref_p_start_date(self):
        jwt = {
            'jti': str(uuid.uuid4()),
            'user_id': '1',
            'form_type': 'a',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '2',
            'period_id': '3',
            'period_str': '2016-01-01',
            'ref_p_start_date': '2016-13-31',
            'ref_p_end_date': '2016-03-03',
            'ru_ref': '2016-04-04',
            'ru_name': 'Apple',
            'return_by': '2016-07-07'
        }
        valid, _ = is_valid_metadata(jwt, {})
        self.assertTrue(valid)
        with self.assertRaises(InvalidTokenException) as ite:
            parse_metadata(jwt, {})
        self.assertIn('incorrect data in token', ite.exception.value)

    def test_is_valid_fails_invalid_ref_p_end_date(self):
        jwt = {
            'jti': str(uuid.uuid4()),
            'user_id': '1',
            'form_type': 'a',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '2',
            'period_id': '3',
            'period_str': '2016-01-01',
            'ref_p_start_date': '2016-12-31',
            'ref_p_end_date': '2016-04-31',
            'ru_ref': '2016-04-04',
            'ru_name': 'Apple',
            'return_by': '2016-07-07'
        }
        valid, _ = is_valid_metadata(jwt, {})
        self.assertTrue(valid)
        with self.assertRaises(InvalidTokenException) as ite:
            parse_metadata(jwt, {})
        self.assertIn('incorrect data in token', ite.exception.value)

    def test_is_valid_fails_invalid_return_by(self):
        jwt = {
            'jti': str(uuid.uuid4()),
            'user_id': '1',
            'form_type': 'a',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '2',
            'period_id': '3',
            'period_str': '2016-01-01',
            'ref_p_start_date': '2016-12-31',
            'ref_p_end_date': '2016-03-31',
            'ru_ref': '2016-04-04',
            'ru_name': 'Apple',
            'return_by': '2016-09-31'
        }
        valid, _ = is_valid_metadata(jwt, {})
        self.assertTrue(valid)
        with self.assertRaises(InvalidTokenException) as ite:
            parse_metadata(jwt, {})
        self.assertIn('incorrect data in token', ite.exception.value)

    def test_is_valid_succeeds_missing_ref_p_end_date(self):
        jwt = {
            'jti': str(uuid.uuid4()),
            'user_id': '1',
            'form_type': 'a',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '2',
            'period_id': '3',
            'period_str': '2016-01-01',
            'ref_p_start_date': '2016-02-02',
            'ru_ref': '2016-04-04',
            'ru_name': 'Apple',
            'return_by': '2016-07-07'
        }
        valid, _ = is_valid_metadata(jwt, {})
        self.assertTrue(valid)

    def test_is_valid_fails_missing_ru_ref(self):
        jwt = {
            'jti': str(uuid.uuid4()),
            'user_id': '1',
            'form_type': 'a',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '2',
            'period_id': '3',
            'period_str': '2016-01-01',
            'ref_p_start_date': '2016-02-02',
            'ref_p_end_date': '2016-03-03',
            'ru_name': 'Apple',
            'return_by': '2016-07-07'
        }
        valid, field = is_valid_metadata(jwt, {})
        self.assertFalse(valid)
        self.assertEqual('ru_ref', field)

    def test_is_valid_fails_missing_ru_name(self):
        jwt = {
            'jti': str(uuid.uuid4()),
            'user_id': '1',
            'form_type': 'a',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '2',
            'period_id': '3',
            'period_str': '2016-01-01',
            'ref_p_start_date': '2016-02-02',
            'ref_p_end_date': '2016-03-03',
            'ru_ref': '2016-04-04',
            'return_by': '2016-07-07'
        }
        valid, field = is_valid_metadata(jwt, {})
        self.assertFalse(valid)
        self.assertEqual('ru_name', field)

    def test_is_valid_fails_missing_return_by(self):
        jwt = {
            'jti': str(uuid.uuid4()),
            'user_id': '1',
            'form_type': 'a',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '2',
            'period_id': '3',
            'period_str': '2016-01-01',
            'ref_p_start_date': '2016-02-02',
            'ref_p_end_date': '2016-03-03',
            'ru_ref': '2016-04-04',
            'ru_name': 'Apple'
        }
        valid, field = is_valid_metadata(jwt, {})
        self.assertFalse(valid)
        self.assertEqual('return_by', field)

    def test_is_valid_does_not_fail_missing_optional_value_in_token(self):
        # tx_id, trad_as and employment_date are optional and might not be in the token
        jwt = {
            'jti': str(uuid.uuid4()),
            'user_id': '1',
            'form_type': 'a',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '2',
            'period_id': '3',
            'period_str': '2016-01-01',
            'ref_p_start_date': '2016-02-02',
            'ref_p_end_date': '2016-03-03',
            'ru_ref': '2016-04-04',
            'ru_name': 'Apple',
            'return_by': '2016-07-07'
        }
        valid, _ = is_valid_metadata(jwt, {})
        self.assertTrue(valid)

    def test_invalid_tx_id(self):
        jwt = {
            'jti': str(uuid.uuid4()),
            'user_id': '1',
            'form_type': 'a',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '2',
            'period_id': '3',
            'period_str': '2016-01-01',
            'ref_p_start_date': '2016-02-02',
            'ref_p_end_date': '2016-03-03',
            'ru_ref': '2016-04-04',
            'ru_name': 'Apple',
            'return_by': '2016-07-07',
            # invalid
            'tx_id': '12121'
        }
        valid, _ = is_valid_metadata(jwt, {})
        self.assertTrue(valid)
        with self.assertRaises(InvalidTokenException) as ite:
            parse_metadata(jwt, {})
        self.assertIn('incorrect data in token', ite.exception.value)

    def test_malformed_tx_id(self):
        jwt = {
            'jti': str(uuid.uuid4()),
            'user_id': '1',
            'form_type': 'a',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '2',
            'period_id': '3',
            'period_str': '2016-01-01',
            'ref_p_start_date': '2016-02-02',
            'ref_p_end_date': '2016-03-03',
            'ru_ref': '2016-04-04',
            'ru_name': 'Apple',
            'return_by': '2016-07-07',
            # one character short
            'tx_id': '83a3db82-bea7-403c-a411-6357ff70f2f'
        }
        valid, _ = is_valid_metadata(jwt, {})
        self.assertTrue(valid)
        with self.assertRaises(InvalidTokenException) as ite:
            parse_metadata(jwt, {})
        self.assertIn('incorrect data in token', ite.exception.value)


if __name__ == '__main__':
    unittest.main()

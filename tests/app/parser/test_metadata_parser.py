import unittest
import uuid

from sdc.crypto.exceptions import InvalidTokenException
from app.storage.metadata_parser import validate_metadata, parse_runner_claims, clean_leading_trailing_spaces
from tests.app.framework.survey_runner_test_case import SurveyRunnerTestCase


class TestMetadataParser(SurveyRunnerTestCase):  # pylint: disable=too-many-public-methods

    def setUp(self):
        super().setUp()
        self.metadata = {
            'tx_id': str(uuid.uuid4()),
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
            'case_id': '1234567890',
            'case_ref': '1000000000000001',
            'account_service_url': 'https://ras.ons.gov.uk'
        }

        self.schema_metadata = [
            {
                'name': 'user_id',
                'validator': 'string'
            },
            {
                'name': 'period_id',
                'validator': 'string'
            }
        ]

        with self.application.test_request_context():
            validate_metadata(self.metadata, self.schema_metadata)

    def test_transaction_id(self):
        with self.application.test_request_context():
            self.assertEqual(self.metadata.get('tx_id'), self.metadata['tx_id'])

    def test_form_type(self):
        with self.application.test_request_context():
            self.assertEqual(self.metadata.get('form_type'), self.metadata['form_type'])

    def test_collection_id(self):
        with self.application.test_request_context():
            self.assertEqual(self.metadata.get('collection_exercise_sid'), self.metadata['collection_exercise_sid'])

    def test_get_eq_id(self):
        with self.application.test_request_context():
            self.assertEqual(self.metadata.get('eq_id'), self.metadata['eq_id'])

    def test_get_period_id(self):
        with self.application.test_request_context():
            self.assertEqual(self.metadata.get('period_id'), self.metadata['period_id'])

    def test_get_period_str(self):
        with self.application.test_request_context():
            self.assertEqual(self.metadata.get('period_str'), self.metadata['period_str'])

    def test_ref_p_start_date(self):
        with self.application.test_request_context():
            self.assertEqual(self.metadata.get('ref_p_start_date'), self.metadata['ref_p_start_date'])

    def test_ref_p_end_date(self):
        with self.application.test_request_context():
            self.assertEqual(self.metadata.get('ref_p_end_date'), self.metadata['ref_p_end_date'])

    def test_ru_ref(self):
        with self.application.test_request_context():
            self.assertEqual(self.metadata.get('ref_p_end_date'), self.metadata['ref_p_end_date'])

    def test_case_id(self):
        with self.application.test_request_context():
            self.assertEqual(self.metadata.get('case_id'), self.metadata['case_id'])

    def test_case_ref(self):
        with self.application.test_request_context():
            self.assertEqual(self.metadata.get('case_ref'), self.metadata['case_ref'])

    def test_account_service_url(self):
        with self.application.test_request_context():
            self.assertEqual(self.metadata.get('account_service_url'), self.metadata['account_service_url'])

    def test_is_valid(self):
        with self.application.test_request_context():
            validate_metadata(self.metadata, self.schema_metadata)

    def test_missing_required_eq_id_in_token(self):
        metadata = {
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

        with self.assertRaises(InvalidTokenException) as ite_key:
            parse_runner_claims(metadata)

        self.assertEqual('Missing key/value for eq_id', str(ite_key.exception))

        with self.assertRaises(InvalidTokenException) as ite_value:
            metadata['eq_id'] = ''
            parse_runner_claims(metadata)

        self.assertEqual('Missing key/value for eq_id', str(ite_value.exception))

    def test_missing_required_metadata_user_id_in_token(self):
        metadata = {
            'jti': str(uuid.uuid4()),
            'form_type': 'a',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '2',
            'period_id': '3',
            'ru_ref': '2016-04-04',
        }

        with self.assertRaises(InvalidTokenException) as ite_key:
            validate_metadata(metadata, self.schema_metadata)

        self.assertEqual('Missing key/value for user_id', str(ite_key.exception))

        with self.assertRaises(InvalidTokenException) as ite_value:
            metadata['user_id'] = ''
            validate_metadata(metadata, self.schema_metadata)

        self.assertEqual('Missing key/value for user_id', str(ite_value.exception))

    def test_missing_required_metadata_period_id_in_token(self):
        metadata = {
            'jti': str(uuid.uuid4()),
            'user_id': '1',
            'form_type': 'a',
            'eq_id': '2',
            'period_str': '2016-01-01',
            'ru_ref': '2016-04-04',
        }

        with self.assertRaises(InvalidTokenException) as ite_key:
            validate_metadata(metadata, self.schema_metadata)

        self.assertEqual('Missing key/value for period_id', str(ite_key.exception))

        with self.assertRaises(InvalidTokenException) as ite_value:
            metadata['period_id'] = ''
            validate_metadata(metadata, self.schema_metadata)

        self.assertEqual('Missing key/value for period_id', str(ite_value.exception))

    def test_missing_required_metadata_return_by_in_token(self):
        metadata = {
            'jti': str(uuid.uuid4()),
            'user_id': '1',
            'form_type': 'a',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '2',
            'period_id': '3',
            'ru_ref': '2016-04-04',
        }

        self.schema_metadata.append({'name': 'return_by', 'validator': 'date'})

        with self.assertRaises(InvalidTokenException) as ite_key:
            validate_metadata(metadata, self.schema_metadata)

        self.assertEqual('Missing key/value for return_by', str(ite_key.exception))

        with self.assertRaises(InvalidTokenException) as ite_value:
            metadata['return_by'] = ''
            validate_metadata(metadata, self.schema_metadata)

        self.assertEqual('Missing key/value for return_by', str(ite_value.exception))

    def test_required_metadata_trad_as_or_ru_name_in_token(self):
        metadata = {
            'jti': str(uuid.uuid4()),
            'user_id': '1',
            'form_type': 'a',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '2',
            'period_id': '3',
            'ru_ref': '2016-04-04'
        }

        self.schema_metadata.append({'name': 'trad_as_or_ru_name', 'validator': 'string'})

        try:
            metadata['ru_name'] = 'ESSENTIAL ENTERPRISE LIMITED'
            validate_metadata(metadata, self.schema_metadata)
        except InvalidTokenException:
            self.fail('Unexpected exception raised.')

        with self.assertRaises(InvalidTokenException) as ite_value:
            metadata['ru_name'] = ''
            validate_metadata(metadata, self.schema_metadata)

        self.assertEqual('Missing key/value for trad_as_or_ru_name', str(ite_value.exception))

    def test_invalid_required_ref_p_start_date(self):
        metadata = {
            'jti': str(uuid.uuid4()),
            'user_id': '1',
            'form_type': 'a',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '2',
            'period_id': '3',
            'ref_p_start_date': '2016-13-31',
            'ru_ref': '2016-04-04',
        }

        self.schema_metadata.append({'name': 'ref_p_start_date', 'validator': 'date'})

        with self.assertRaises(InvalidTokenException) as ite:
            validate_metadata(metadata, self.schema_metadata)

        self.assertEqual('incorrect data in token', str(ite.exception))

    def test_invalid_tx_id(self):
        metadata = {
            'jti': str(uuid.uuid4()),
            'user_id': '1',
            'form_type': 'a',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '2',
            'period_id': '3',
            'ru_ref': '2016-04-04',
            'case_id': str(uuid.uuid4()),
            # invalid
            'tx_id': '12121'
        }

        with self.assertRaises(InvalidTokenException) as ite:
            parse_runner_claims(metadata)

        self.assertEqual('incorrect data in token', str(ite.exception))

    def test_malformed_tx_id(self):
        metadata = {
            'jti': str(uuid.uuid4()),
            'user_id': '1',
            'form_type': 'a',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '2',
            'period_id': '3',
            'ru_ref': '2016-04-04',
            'case_id': str(uuid.uuid4()),
            # one character short
            'tx_id': '83a3db82-bea7-403c-a411-6357ff70f2f'
        }

        with self.assertRaises(InvalidTokenException) as ite:
            parse_runner_claims(metadata)

        self.assertEqual('incorrect data in token', str(ite.exception))

    def test_generated_tx_id_format(self):

        metadata = {
            'tx_id': str(uuid.uuid4()),
            'jti': str(uuid.uuid4()),
            'user_id': '1',
            'form_type': 'a',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '2',
            'period_id': '3',
            'ru_ref': '2016-04-04',
            'case_id': str(uuid.uuid4())
        }

        parsed = parse_runner_claims(metadata)
        tx_id = parsed['tx_id']

        self.assertEqual(tx_id, str(uuid.UUID(tx_id)))

    def test_invalid_schema_metadata(self):
        metadata = {
            'jti': str(uuid.uuid4()),
            'user_id': '1',
            'form_type': 'a',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '2',
            'period_id': '3',
            'ru_ref': '2016-04-04',
            'period_str': 'May 2016',
            'case_id': str(uuid.uuid4())
        }

        self.schema_metadata.append({'name': 'period_id', 'validator': 'invalidValidator'})

        with self.assertRaises(KeyError) as ite:
            validate_metadata(metadata, self.schema_metadata)

        self.assertEqual('Invalid validator for schema metadata - invalidValidator', ite.exception.args[0])

    def test_clean_leading_trailing_spaces(self):
        metadata = self.metadata.copy()
        metadata['trad_as'] = ' '
        metadata['ru_name'] = '   Apple   '

        metadata = clean_leading_trailing_spaces(metadata)

        self.assertEqual(metadata['trad_as'], '')
        self.assertEqual(metadata['ru_name'], 'Apple')


if __name__ == '__main__':
    unittest.main()

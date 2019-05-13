import datetime
import unittest
import uuid

from flask_login import LoginManager
from sdc.crypto.exceptions import InvalidTokenException

from app.storage.metadata_parser import (
    boolean_parser,
    clean_leading_trailing_spaces,
    iso_8601_date_parser,
    optional_string_parser,
    parse_runner_claims,
    string_parser,
    validate_metadata,
    uuid_4_parser,
)
from tests.app.app_context_test_case import AppContextTestCase

login_manager = LoginManager()

class TestMetadataParser(
    AppContextTestCase
):  # pylint: disable=too-many-public-methods
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
            'response_id': '1234567890123456',
            'return_by': '2016-07-07',
            'case_id': '1234567890',
            'case_ref': '1000000000000001',
            'account_service_url': 'https://ras.ons.gov.uk',
        }

        self.schema_metadata = [
            {'name': 'user_id', 'validator': 'string'},
            {'name': 'period_id', 'validator': 'string'},
        ]

        with self._app.test_request_context():
            validate_metadata(self.metadata, self.schema_metadata)

    def test_transaction_id(self):
        with self._app.test_request_context():
            self.assertEqual(self.metadata.get('tx_id'), self.metadata['tx_id'])

    def test_form_type(self):
        with self._app.test_request_context():
            self.assertEqual(self.metadata.get('form_type'), self.metadata['form_type'])

    def test_collection_id(self):
        with self._app.test_request_context():
            self.assertEqual(
                self.metadata.get('collection_exercise_sid'),
                self.metadata['collection_exercise_sid'],
            )

    def test_get_eq_id(self):
        with self._app.test_request_context():
            self.assertEqual(self.metadata.get('eq_id'), self.metadata['eq_id'])

    def test_get_period_id(self):
        with self._app.test_request_context():
            self.assertEqual(self.metadata.get('period_id'), self.metadata['period_id'])

    def test_get_period_str(self):
        with self._app.test_request_context():
            self.assertEqual(
                self.metadata.get('period_str'), self.metadata['period_str']
            )

    def test_ref_p_start_date(self):
        with self._app.test_request_context():
            self.assertEqual(
                self.metadata.get('ref_p_start_date'), self.metadata['ref_p_start_date']
            )

    def test_ref_p_end_date(self):
        with self._app.test_request_context():
            self.assertEqual(
                self.metadata.get('ref_p_end_date'), self.metadata['ref_p_end_date']
            )

    def test_ru_ref(self):
        with self._app.test_request_context():
            self.assertEqual(
                self.metadata.get('ref_p_end_date'), self.metadata['ref_p_end_date']
            )

    def test_case_id(self):
        with self._app.test_request_context():
            self.assertEqual(self.metadata.get('case_id'), self.metadata['case_id'])

    def test_case_ref(self):
        with self._app.test_request_context():
            self.assertEqual(self.metadata.get('case_ref'), self.metadata['case_ref'])

    def test_account_service_url(self):
        with self._app.test_request_context():
            self.assertEqual(
                self.metadata.get('account_service_url'),
                self.metadata['account_service_url'],
            )

    def test_is_valid(self):
        with self._app.test_request_context():
            validate_metadata(self.metadata, self.schema_metadata)

    def test_missing_required_eq_id_in_token(self):
        schema_metadata = [
            {'name': 'user_id', 'validator': 'string'},
            {'name': 'period_id', 'validator': 'string'},
            {'name': 'eq_id', 'validator': 'string'},
        ]

        del self.metadata['eq_id']

        with self.assertRaises(InvalidTokenException) as ite_key:
            validate_metadata(self.metadata, schema_metadata)

        self.assertEqual(
            'Missing required key eq_id from claims', str(ite_key.exception)
        )

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

        self.assertEqual(
            'Missing required key user_id from claims', str(ite_key.exception)
        )

        with self.assertRaises(InvalidTokenException) as ite_value:
            metadata['user_id'] = ''
            validate_metadata(metadata, self.schema_metadata)

        self.assertEqual(
            'incorrect data in token for user_id', str(ite_value.exception)
        )

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

        self.assertEqual(
            'Missing required key period_id from claims', str(ite_key.exception)
        )

        with self.assertRaises(InvalidTokenException) as ite_value:
            metadata['period_id'] = ''
            validate_metadata(metadata, self.schema_metadata)

        self.assertEqual(
            'incorrect data in token for period_id', str(ite_value.exception)
        )

    def test_missing_metadata_address_line_in_token(self):
        schema_metadata = [
            {'name': 'user_id', 'validator': 'string'},
            {'name': 'period_id', 'validator': 'string'},
            {'name': 'address_line1', 'validator': 'optional_string'},
            {'name': 'address_line2', 'validator': 'optional_string'},
            {'name': 'locality', 'validator': 'optional_string'},
            {'name': 'town_name', 'validator': 'optional_string'},
            {'name': 'postcode', 'validator': 'optional_string'},
            {'name': 'display_address', 'validator': 'string'},
        ]

        with self.assertRaises(InvalidTokenException) as ite_key:
            validate_metadata(self.metadata, schema_metadata)

        self.assertEqual(
            'Missing required key address_line1 from claims', str(ite_key.exception)
        )

        self.metadata['address_line1'] = '68 Testing Road'
        self.metadata['address_line2'] = ''
        self.metadata['locality'] = ''
        self.metadata['town_name'] = 'Goatmount'
        self.metadata['postcode'] = 'PE12 4GH'
        self.metadata['display_address'] = '68 Testing Road, Goatmount, PE12 4GH'

        validate_metadata(self.metadata, schema_metadata)

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

        self.assertEqual(
            'Missing required key return_by from claims', str(ite_key.exception)
        )

        with self.assertRaises(InvalidTokenException) as ite_value:
            metadata['return_by'] = ''
            validate_metadata(metadata, self.schema_metadata)

        self.assertEqual(
            'incorrect data in token for return_by', str(ite_value.exception)
        )

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

        self.assertEqual(
            'incorrect data in token for ref_p_start_date', str(ite.exception)
        )

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
            'tx_id': '12121',
        }

        with self.assertRaises(InvalidTokenException) as ite:
            parse_runner_claims(metadata)

        self.assertEqual('incorrect data in token for tx_id', str(ite.exception))

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
            'tx_id': '83a3db82-bea7-403c-a411-6357ff70f2f',
        }

        with self.assertRaises(InvalidTokenException) as ite:
            parse_runner_claims(metadata)

        self.assertEqual('incorrect data in token for tx_id', str(ite.exception))

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
            'response_id': '1234567890123456',
            'case_id': str(uuid.uuid4()),
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
            'response_id': '1234567890123456',
            'period_str': 'May 2016',
            'case_id': str(uuid.uuid4()),
        }

        self.schema_metadata.append(
            {'name': 'period_id', 'validator': 'invalidValidator'}
        )

        with self.assertRaises(KeyError) as ite:
            validate_metadata(metadata, self.schema_metadata)

        self.assertEqual(
            'Invalid validator for schema metadata - invalidValidator',
            ite.exception.args[0],
        )

    def test_clean_leading_trailing_spaces(self):
        metadata = self.metadata.copy()
        metadata['trad_as'] = ' '
        metadata['ru_name'] = '   Apple   '

        metadata = clean_leading_trailing_spaces(metadata)

        self.assertEqual(metadata['trad_as'], '')
        self.assertEqual(metadata['ru_name'], 'Apple')

    def test_date_parser_valid(self):
        test_date = '2016-05-01'
        validator = iso_8601_date_parser(test_date)
        self.assertEqual(datetime.datetime(2016, 5, 1, 0, 0), validator)

    def test_date_parser_invalid_format(self):
        test_date = '2016'
        with self.assertRaises(ValueError) as error:
            iso_8601_date_parser(test_date)
        self.assertEqual(
            "time data '2016' does not match format '%Y-%m-%d'", error.exception.args[0]
        )

    def test_date_parser_invalid_empty_string(self):
        test_date = ''
        with self.assertRaises(ValueError) as error:
            iso_8601_date_parser(test_date)
        self.assertEqual(
            "time data '' does not match format '%Y-%m-%d'", error.exception.args[0]
        )

    def test_uuid_parser_valid(self):
        test_uuid = '19162b10-96b6-4051-99d6-70183ca23b38'
        validator = uuid_4_parser(test_uuid)
        self.assertEqual('19162b10-96b6-4051-99d6-70183ca23b38', validator)

    def test_uuid_parser_invalid_uuid(self):
        test_uuid = 'test'
        with self.assertRaises(ValueError) as error:
            uuid_4_parser(test_uuid)
        self.assertEqual(
            'badly formed hexadecimal UUID string', error.exception.args[0]
        )

    def test_boolean_parser_True_valid(self):
        test_boolean = True
        validator = boolean_parser(test_boolean)
        self.assertEqual(True, validator)

    def test_boolean_parser_False_valid(self):
        test_boolean = False
        validator = boolean_parser(test_boolean)
        self.assertEqual(False, validator)

    def test_boolean_parser_invalid_bool(self):
        test_boolean = 'test'
        with self.assertRaises(TypeError) as error:
            boolean_parser(test_boolean)
        self.assertEqual('Claim was not of type `bool`', error.exception.args[0])

    def test_string_validator_valid(self):
        test_string = 'test a normal string'
        validator = string_parser(test_string)
        self.assertEqual('test a normal string', validator)

    def test_string_validator_invalid_empty_string(self):
        test_string = ''
        with self.assertRaises(TypeError) as error:
            string_parser(test_string)
        self.assertEqual('Claim not a valid string value', error.exception.args[0])

    def test_optional_string_valid(self):
        test_optional_string = 'test valid string'
        validator = optional_string_parser(test_optional_string)
        self.assertEqual('test valid string', validator)

    def test_optional_string_valid_empty_string(self):
        test_optional_string = ''
        validator = optional_string_parser(test_optional_string)
        self.assertEqual('', validator)

    def test_optional_string_invalid(self):
        test_optional_string = None
        with self.assertRaises(TypeError) as error:
            optional_string_parser(test_optional_string)
        self.assertEqual('Claim not a valid/empty string', error.exception.args[0])


if __name__ == '__main__':
    unittest.main()

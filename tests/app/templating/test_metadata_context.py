from app.storage.metadata_parser import parse_metadata
from app.templating.metadata_context import build_metadata_context
from tests.app.framework.survey_runner_test_case import SurveyRunnerTestCase

STRING_PROPERTIES = 'user_id', 'form_type', 'collection_exercise_sid',\
                    'eq_id', 'period_id', 'ru_ref', 'ru_name', 'trad_as',\
                    'transaction_id', 'region_code', 'period_str'

DATE_PROPERTIES = 'ref_p_start_date', 'ref_p_end_date', 'return_by'


class TestMetadataContext(SurveyRunnerTestCase):
    def setUp(self):
        super().setUp()
        self.jwt = {
            'user_id': '1',
            'form_type': 'a',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '2',
            'period_id': '3',
            'period_str': '2016-01-14',
            'ref_p_start_date': '2016-02-22',
            'ref_p_end_date': '2016-03-30',
            'ru_ref': '178324',
            'ru_name': 'Apple',
            'trad_as': 'Apple',
            'return_by': '2016-07-17',
            'transaction_id': '4ec3aa9e-e8ac-4c8d-9793-6ed88b957c2f'
        }

    def test_build_metadata_context(self):
        with self.application.test_request_context():
            metadata = parse_metadata(self.jwt, required_metadata={})

        metadata_context = build_metadata_context(metadata)

        self.assertIsNotNone(metadata_context)
        self.assertEqual('2016-07-17', metadata_context['return_by'])
        self.assertEqual('2016-02-22', metadata_context['start_date'])
        self.assertEqual('2016-03-30', metadata_context['end_date'])
        self.assertIsNone(metadata_context['employment_date'])
        self.assertIsNone(metadata_context['region_code'])
        self.assertEqual(self.jwt['period_str'], metadata_context['period_str'])
        self.assertEqual(self.jwt['ru_ref'], metadata_context['respondent_id'])
        self.assertEqual(self.jwt['ru_name'], metadata_context['name'])
        self.assertEqual(self.jwt['trad_as'], metadata_context['trading_as'])

    def test_defend_against_XSS_attack(self):
        jwt = self.jwt.copy()
        escaped_bad_characters = r'&lt;&#34;&gt;\\'

        for key in STRING_PROPERTIES:
            jwt[key] = '<">\\'

        with self.application.test_request_context():
            metadata = parse_metadata(jwt, required_metadata={})

        metadata_context = build_metadata_context(metadata)

        self.assertEqual(escaped_bad_characters, metadata_context['respondent_id'])
        self.assertEqual(escaped_bad_characters, metadata_context['name'])
        self.assertEqual(escaped_bad_characters, metadata_context['trading_as'])

        self.assertEqual(escaped_bad_characters, metadata_context['region_code'])
        self.assertEqual(escaped_bad_characters, metadata_context['period_str'])
        self.assertEqual(escaped_bad_characters, metadata_context['eq_id'])
        self.assertEqual(escaped_bad_characters, metadata_context['collection_id'])
        self.assertEqual(escaped_bad_characters, metadata_context['form_type'])

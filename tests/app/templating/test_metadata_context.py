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
            metadata = parse_metadata(self.jwt)

        render_data = build_metadata_context(metadata)

        self.assertIsNotNone(render_data)

        survey_data = render_data['survey']
        self.assertIsNotNone(survey_data)

        self.assertEqual('2016-07-17', survey_data['return_by'])
        self.assertEqual('2016-02-22', survey_data['start_date'])
        self.assertEqual('2016-03-30', survey_data['end_date'])
        self.assertIsNone(survey_data['employment_date'])
        self.assertIsNone(survey_data['region_code'])
        self.assertEqual(self.jwt['period_str'], survey_data['period_str'])

        respondent = render_data['respondent']
        self.assertIsNotNone(respondent)

        self.assertEqual(self.jwt['ru_ref'], respondent['respondent_id'])
        self.assertEqual(self.jwt['ru_name'], respondent['name'])
        self.assertEqual(self.jwt['trad_as'], respondent['trading_as'])

    def test_defend_against_XSS_attack(self):
        jwt = self.jwt.copy()
        escaped_bad_characters = r'&lt;&#34;&gt;\\'

        for key in STRING_PROPERTIES:
            jwt[key] = '<">\\'

        with self.application.test_request_context():
            metadata = parse_metadata(jwt)

        render_data = build_metadata_context(metadata)

        respondent = render_data['respondent']
        self.assertEqual(escaped_bad_characters, respondent['respondent_id'])
        self.assertEqual(escaped_bad_characters, respondent['name'])
        self.assertEqual(escaped_bad_characters, respondent['trading_as'])

        survey = render_data['survey']
        self.assertEqual(escaped_bad_characters, survey['region_code'])
        self.assertEqual(escaped_bad_characters, survey['period_str'])
        self.assertEqual(escaped_bad_characters, survey['eq_id'])
        self.assertEqual(escaped_bad_characters, survey['collection_id'])
        self.assertEqual(escaped_bad_characters, survey['form_type'])

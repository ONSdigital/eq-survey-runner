from app.parser.metadata_parser import parse_metadata
from app.templating.metadata_context import build_metadata_context
from tests.app.framework.sr_unittest import SurveyRunnerTestCase


class TestMetadataContext(SurveyRunnerTestCase):
    def setUp(self):
        super().setUp()
        self.jwt = {
            "user_id": "1",
            "form_type": "a",
            "collection_exercise_sid": "test-sid",
            "eq_id": "2",
            "period_id": "3",
            "period_str": "2016-01-01",
            "ref_p_start_date": "2016-02-02",
            "ref_p_end_date": "2016-03-03",
            "ru_ref": "178324",
            "ru_name": "Apple",
            "trad_as": "Apple",
            "return_by": "2016-07-07",
            "transaction_id": "4ec3aa9e-e8ac-4c8d-9793-6ed88b957c2f"
        }
        with self.application.test_request_context():
            self.metadata = parse_metadata(self.jwt)

    def test_build_metadata_context(self):
        render_data = build_metadata_context(self.metadata)

        self.assertIsNotNone(render_data)

        survey_data = render_data['survey']
        self.assertIsNotNone(survey_data)

        self.assertEqual('7 July 2016', survey_data['return_by'].strftime('%-d %B %Y'))
        self.assertEqual('2 February 2016', survey_data['start_date'].strftime('%-d %B %Y'))
        self.assertEqual('3 March 2016', survey_data['end_date'].strftime('%-d %B %Y'))
        self.assertIsNone(survey_data['employment_date'])
        self.assertIsNone(survey_data['region_code'])
        self.assertEqual(self.jwt["period_str"], survey_data['period_str'])

        respondent = render_data['respondent']
        self.assertIsNotNone(respondent)

        self.assertEqual(self.jwt["ru_ref"], respondent['respondent_id'])
        self.assertEqual(self.jwt["ru_name"], respondent['address']['name'])
        self.assertEqual(self.jwt["trad_as"], respondent['address']['trading_as'])

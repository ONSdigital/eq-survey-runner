from app.parser.metadata_parser import parse_metadata
from app.templating.metadata_template_preprocessor import MetaDataTemplatePreprocessor
from tests.app.framework.sr_unittest import SurveyRunnerTestCase


class TestMetadataTemplatePreprocessor(SurveyRunnerTestCase):
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

    def get_metadata(self):
          return self.metadata

    def test_build_view_data(self):
        metadata_preprocessor = MetaDataTemplatePreprocessor()
        metadata_preprocessor._get_metadata = self.get_metadata

        render_data = metadata_preprocessor.build_metadata(self.questionnaire)

        self.assertIsNotNone(render_data)

        survey_data = render_data['survey']
        self.assertIsNotNone(survey_data)

        self.assertEqual(self.questionnaire.title, survey_data['title'])
        self.assertEqual(self.questionnaire.survey_id, survey_data['survey_code'])
        self.assertEqual(self.questionnaire.introduction.information_to_provide, survey_data['information_to_provide'])
        self.assertEqual(self.questionnaire.theme, survey_data['theme'])
        self.assertEqual('7 July 2016', survey_data['return_by'])
        self.assertEqual('2 February 2016', survey_data['start_date'])
        self.assertEqual('3 March 2016', survey_data['end_date'])
        self.assertIsNone(survey_data['employment_date'])
        self.assertEqual(self.jwt["period_str"], survey_data['period_str'])

        respondent = render_data['respondent']
        self.assertIsNotNone(respondent)

        self.assertEqual(self.jwt["ru_ref"], respondent['respondent_id'])
        self.assertEqual(self.jwt["ru_name"], respondent['address']['name'])
        self.assertEqual(self.jwt["trad_as"], respondent['address']['trading_as'])

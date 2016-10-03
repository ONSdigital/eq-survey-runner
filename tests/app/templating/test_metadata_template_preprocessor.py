from app.templating.metadata_template_preprocessor import MetaDataTemplatePreprocessor
from app.authentication.user import User
from app.metadata.metadata_store import MetaDataStore, MetaDataConstants

from tests.app.framework.sr_unittest import SurveyRunnerTestCase


class TestMetadataTemplatePreprocessor(SurveyRunnerTestCase):
    def setUp(self):
        super().setUp()
        self.jwt = {
            MetaDataConstants.USER_ID.claim_id: "1",
            MetaDataConstants.FORM_TYPE.claim_id: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetaDataConstants.EQ_ID.claim_id: "2",
            MetaDataConstants.PERIOD_ID.claim_id: "3",
            MetaDataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetaDataConstants.RU_REF.claim_id: "178324",
            MetaDataConstants.RU_NAME.claim_id: "Apple",
            MetaDataConstants.TRAD_AS.claim_id: "Apple",
            MetaDataConstants.RETURN_BY.claim_id: "2016-07-07",
            MetaDataConstants.TRANSACTION_ID.claim_id: "4ec3aa9e-e8ac-4c8d-9793-6ed88b957c2f"
        }
        with self.application.test_request_context():
            user = User("1", "2")
            self.metadata_store = MetaDataStore.save_instance(user, self.jwt)

    def get_metadata_store(self):
          return self.metadata_store

    def test_build_view_data(self):
        metadata_preprocessor = MetaDataTemplatePreprocessor()
        metadata_preprocessor._get_metadata = self.get_metadata_store

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
        self.assertEqual(self.jwt[MetaDataConstants.PERIOD_STR.claim_id], survey_data['period_str'])

        respondent = render_data['respondent']
        self.assertIsNotNone(respondent)

        self.assertEqual(self.jwt[MetaDataConstants.RU_REF.claim_id], respondent['respondent_id'])
        self.assertEqual(self.jwt[MetaDataConstants.RU_NAME.claim_id], respondent['address']['name'])
        self.assertEqual(self.jwt[MetaDataConstants.TRAD_AS.claim_id], respondent['address']['trading_as'])

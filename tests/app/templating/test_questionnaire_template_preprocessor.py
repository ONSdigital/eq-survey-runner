from tests.app.framework.sr_unittest import SurveyRunnerTestCase
from app.templating.questionnaire_template_preprocessor import QuestionnaireTemplatePreprocessor
from app.authentication.user import User
from app.data_model.metadata_store import MetaDataStore, MetaDataConstants
from app.templating.metadata_template_preprocessor import MetaDataTemplatePreprocessor
from app.questionnaire_state.node import Node
from app.questionnaire_state.block import Block


class TestQuestionnaireTemplatePreprocessor(SurveyRunnerTestCase):

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
        block = Block("1", None)
        node = Node("1", block)

        questionnaire_template_preprocessor = QuestionnaireTemplatePreprocessor()
        original_get_metadata_method = MetaDataTemplatePreprocessor._get_metadata
        MetaDataTemplatePreprocessor._get_metadata = self.get_metadata_store

        render_data = questionnaire_template_preprocessor.build_view_data(node, self.questionnaire)
        self.assertIsNotNone(render_data)
        self.assertEqual(block, render_data['content'])

        self.assertIsNotNone(render_data['meta'])

        MetaDataTemplatePreprocessor._get_metadata = original_get_metadata_method





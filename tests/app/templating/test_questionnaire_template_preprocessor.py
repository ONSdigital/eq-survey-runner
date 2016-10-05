from app.parser.metadata_parser import MetadataParser, MetadataConstants
from app.questionnaire_state.block import Block
from app.questionnaire_state.node import Node
from app.templating.metadata_template_preprocessor import MetaDataTemplatePreprocessor
from app.templating.questionnaire_template_preprocessor import QuestionnaireTemplatePreprocessor
from tests.app.framework.sr_unittest import SurveyRunnerTestCase


class TestQuestionnaireTemplatePreprocessor(SurveyRunnerTestCase):

    def setUp(self):
        super().setUp()
        self.jwt = {
            MetadataConstants.USER_ID.claim_id: "1",
            MetadataConstants.FORM_TYPE.claim_id: "a",
            MetadataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetadataConstants.EQ_ID.claim_id: "2",
            MetadataConstants.PERIOD_ID.claim_id: "3",
            MetadataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetadataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetadataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetadataConstants.RU_REF.claim_id: "178324",
            MetadataConstants.RU_NAME.claim_id: "Apple",
            MetadataConstants.TRAD_AS.claim_id: "Apple",
            MetadataConstants.RETURN_BY.claim_id: "2016-07-07",
            MetadataConstants.TRANSACTION_ID.claim_id: "4ec3aa9e-e8ac-4c8d-9793-6ed88b957c2f"
        }
        with self.application.test_request_context():
            self.metadata = MetadataParser.parse_metadata(self.jwt)

    def get_metadata_store(self):
        return self.metadata

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





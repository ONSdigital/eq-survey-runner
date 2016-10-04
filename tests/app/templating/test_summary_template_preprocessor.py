from tests.app.framework.sr_unittest import SurveyRunnerTestCase
from app.templating.summary_template_preprocessor import SummaryTemplatePreprocessor
from app.authentication.user import User
from app.data_model.metadata_store import MetaDataStore, MetaDataConstants
from app.templating.metadata_template_preprocessor import MetaDataTemplatePreprocessor
from app.questionnaire_state.node import Node
from app.questionnaire_state.block import Block
from app.questionnaire_state.section import Section


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
            self.metadata_store = MetaDataStore.save_instance("1", "2", self.jwt)

    def get_metadata_store(self):
        return self.metadata_store

    # Blocks are recreated from the sections within
    def test_build_view_data(self):
        section1 = Section("4", None)
        section2 = Section("5", None)
        section3 = Section("6", None)

        section1.title = "Title 1"
        section2.title = "Title 2"
        section3.title = "Title 3"

        block1 = Block("1", None)
        block2 = Block("2", None)

        block1.sections = [section1, section2]
        block2.sections = [section3]

        self.questionnaire.register(block1)
        self.questionnaire.register(block2)

        self.questionnaire.register(section1)
        self.questionnaire.register(section2)
        self.questionnaire.register(section3)

        node1 = Node("1", block1)
        node2 = Node("2", block2)

        node1.next = node2

        summary_template_preprocessor = SummaryTemplatePreprocessor()
        original_get_metadata_method = MetaDataTemplatePreprocessor._get_metadata
        MetaDataTemplatePreprocessor._get_metadata = self.get_metadata_store

        render_data = summary_template_preprocessor.build_view_data(node1, self.questionnaire)
        self.assertIsNotNone(render_data)
        blocks = render_data['content']

        # Pull back all the section states from the blocks
        states = [block.state for block in blocks]

        self.assertTrue(section1 in states)
        self.assertTrue(section2 in states)
        self.assertTrue(section3 in states)

        self.assertIsNotNone(render_data['meta'])

        MetaDataTemplatePreprocessor._get_metadata = original_get_metadata_method

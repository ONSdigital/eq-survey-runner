from app.parser.metadata_parser import parse_metadata
from tests.app.framework.sr_unittest import SurveyRunnerTestCase
from app.templating.summary_template_preprocessor import SummaryTemplatePreprocessor

from app.templating.metadata_template_preprocessor import MetaDataTemplatePreprocessor
from app.questionnaire_state.node import Node
from app.questionnaire_state.state_block import StateBlock
from app.questionnaire_state.state_section import StateSection



class TestQuestionnaireTemplatePreprocessor(SurveyRunnerTestCase):

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

    # Blocks are recreated from the sections within
    def test_build_view_data(self):
        section1 = StateSection("4", None)
        section2 = StateSection("5", None)
        section3 = StateSection("6", None)

        section1.title = "Title 1"
        section2.title = "Title 2"
        section3.title = "Title 3"

        block1 = StateBlock("1", None)
        block2 = StateBlock("2", None)

        block1.sections = [section1, section2]
        block2.sections = [section3]

        self.questionnaire.register(block1)
        self.questionnaire.register(block2)

        self.questionnaire.register(section1)
        self.questionnaire.register(section2)
        self.questionnaire.register(section3)

        node1 = Node("1")
        node2 = Node("2")
        state = StateBlock("1", None)
        node1.next = node2

        questionnaire_template_preprocessor = SummaryTemplatePreprocessor()
        original_get_metadata_method = MetaDataTemplatePreprocessor._get_metadata

        MetaDataTemplatePreprocessor._get_metadata = self.get_metadata
        state_items = [state]
        render_data = questionnaire_template_preprocessor.build_view_data(node1, self.questionnaire, state_items)
        self.assertIsNotNone(render_data)
        #self.assertEqual(state, render_data['content'])

        #self.assertIsNotNone(render_data['meta'])

        MetaDataTemplatePreprocessor._get_metadata = original_get_metadata_method

from app.parser.metadata_parser import parse_metadata
from tests.app.framework.sr_unittest import SurveyRunnerTestCase
from app.templating.questionnaire_template_preprocessor import QuestionnaireTemplatePreprocessor

from app.templating.metadata_template_preprocessor import MetaDataTemplatePreprocessor
from app.questionnaire_state.node import Node
from app.questionnaire_state.state_block import StateBlock



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

    def test_build_view_data(self):
        block = StateBlock("1", None)
        node = Node("1")

        questionnaire_template_preprocessor = QuestionnaireTemplatePreprocessor()
        original_get_metadata_method = MetaDataTemplatePreprocessor._get_metadata

        MetaDataTemplatePreprocessor._get_metadata = self.get_metadata
        state_items = [block]
        render_data = questionnaire_template_preprocessor.build_view_data(node, self.questionnaire, state_items)

        self.assertIsNotNone(render_data)
        self.assertEqual(block, render_data['content'])

        self.assertIsNotNone(render_data['meta'])

        MetaDataTemplatePreprocessor._get_metadata = original_get_metadata_method





from unittest.mock import MagicMock

from app.data_model.answer_store import AnswerStore
from app.data_model.list_store import ListStore
from app.data_model.progress_store import ProgressStore, CompletionStatus
from app.data_model.questionnaire_store import QuestionnaireStore
from app.questionnaire.location import Location
from app.views.handlers.summary import Summary
from app.utilities.schema import load_schema_from_name
from tests.app.app_context_test_case import AppContextTestCase


class TestStandardSummaryHandler(AppContextTestCase):
    def setUp(self):
        super().setUp()
        self.metadata = {
            'return_by': '2016-10-10',
            'ref_p_start_date': '2016-10-10',
            'ref_p_end_date': '2016-10-10',
            'ru_ref': 'def123',
            'response_id': 'abc123',
            'ru_name': 'Mr Cloggs',
            'trad_as': 'Samsung',
            'tx_id': '12345678-1234-5678-1234-567812345678',
            'period_str': '201610',
            'employment_date': '2016-10-10',
            'collection_exercise_sid': '789',
            'schema_name': '0000_1',
        }
        self.language = 'en'

    def check_context(self, context):
        self.assertEqual(len(context), 1)
        self.assertTrue(
            'summary' in context, 'Key value {} missing from context'.format('summary')
        )

        summary_context = context['summary']
        for key_value in ('groups', 'answers_are_editable', 'summary_type'):
            self.assertTrue(
                key_value in summary_context,
                "Key value {} missing from context['summary']".format(key_value),
            )

    def check_groups(self, groups):
        for group in groups:
            self.assertTrue('id' in group)
            self.assertTrue('blocks' in group)
            for block in group['blocks']:
                self.assertTrue('question' in block)
                self.assertTrue('title' in block['question'])
                self.assertTrue('answers' in block['question'])
                for answer in block['question']['answers']:
                    self.assertTrue('id' in answer)
                    self.assertTrue('value' in answer)
                    self.assertTrue('type' in answer)


class TestSummaryHandler(TestStandardSummaryHandler):
    def setUp(self):
        super().setUp()
        self.schema = load_schema_from_name('test_summary')
        self.answer_store = AnswerStore()
        self.list_store = ListStore()
        self.block_type = 'Summary'
        self.rendered_block = {
            'parent_id': 'summary-group',
            'id': 'summary',
            'type': 'Summary',
            'collapsible': True,
        }
        self.language = 'en'
        self.current_location = Location(
            section_id='default-section', block_id='summary'
        )

        storage = MagicMock()
        storage.get_user_data = MagicMock(return_value=('{}', 1))
        storage.add_or_update = MagicMock()

        self.questionnaire_store = QuestionnaireStore(storage)
        self.questionnaire_store.answer_store = AnswerStore(
            [
                {'answer_id': 'radio-answer', 'value': 'Eggs', 'list_item_id': None},
                {'answer_id': 'test-currency', 'value': 1, 'list_item_id': None},
                {'answer_id': 'square-kilometres', 'value': 1, 'list_item_id': None},
                {'answer_id': 'test-decimal', 'value': 1, 'list_item_id': None},
                {'answer_id': 'dessert', 'value': 'Cake', 'list_item_id': None},
            ]
        )
        self.questionnaire_store.progress_store = ProgressStore(
            [
                {
                    'section_id': 'default-section',
                    'list_item_id': None,
                    'status': CompletionStatus.COMPLETED,
                    'locations': [
                        {'section_id': 'default-section', 'block_id': 'radio'},
                        {
                            'section_id': 'default-section',
                            'block_id': 'test-number-block',
                        },
                        {'section_id': 'default-section', 'block_id': 'dessert-block'},
                    ],
                }
            ]
        )

    def test_build_summary_rendering_context(self):
        summary = Summary(
            self.schema,
            self.questionnaire_store,
            self.language,
            self.current_location,
            None,
        )
        context = summary.get_context()

        self.check_groups(context['summary']['groups'])

    def test_build_view_context_for_summary(self):
        summary = Summary(
            self.schema,
            self.questionnaire_store,
            self.language,
            self.current_location,
            None,
        )
        context = summary.get_context()

        self.check_context(context)
        self.check_groups(context['summary']['groups'])

        self.assertEqual(len(context['summary']), 5)
        self.assertTrue('is_view_submission_response_enabled' in context['summary'])
        self.assertTrue('collapsible' in context['summary'])

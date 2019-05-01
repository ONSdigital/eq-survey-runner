import simplejson as json
from mock import Mock

from app.data_model.answer_store import AnswerStore
from app.data_model.list_store import ListStore
from app.data_model.questionnaire_store import QuestionnaireStore
from app.questionnaire.location import Location
from app.templating.view_context import build_view_context
from app.utilities.schema import load_schema_from_params
from app.views.questionnaire import get_page_title_for_location
from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaire(IntegrationTestCase):
    def setUp(self):
        super().setUp()
        self._application_context = self._application.app_context()
        self._application_context.push()

        storage = Mock()
        data = {
            'METADATA': 'test',
            'ANSWERS': [],
            'COMPLETED_BLOCKS': []
        }
        storage.get_user_data = Mock(return_value=(json.dumps(data), QuestionnaireStore.LATEST_VERSION))

        self.question_store = QuestionnaireStore(storage)
        self.mock_context = {'block': {'question': {'title': 'Testing title'}}}

    def tearDown(self):
        self._application_context.pop()

    def test_given_introduction_page_when_get_page_title_then_defaults_to_survey_title(self):
        # Given
        schema = load_schema_from_params('test', 'final_confirmation')

        # When
        page_title = get_page_title_for_location(schema, Location('introduction'), self.mock_context)

        # Then
        self.assertEqual(page_title, 'Final confirmation to submit')

    def test_given_interstitial_page_when_get_page_title_then_group_title_and_survey_title(self):
        # Given
        schema = load_schema_from_params('test', 'interstitial_page')

        # When
        page_title = get_page_title_for_location(schema, Location('breakfast-interstitial'), self.mock_context)

        # Then
        self.assertEqual(page_title, 'Favourite food - Interstitial Pages')

    def test_given_questionnaire_page_when_get_page_title_then_question_title_and_survey_title(self):
        # Given
        schema = load_schema_from_params('test', 'final_confirmation')

        # When
        page_title = get_page_title_for_location(schema, Location('breakfast'), self.mock_context)

        # Then
        self.assertEqual(page_title, 'Testing title - Final confirmation to submit')

    def test_build_view_context_for_calculation_summary(self):
        # Given
        schema = load_schema_from_params('test', 'calculated_summary')
        block = schema.get_block('currency-total-playback-with-fourth')
        metadata = {
            'tx_id': '12345678-1234-5678-1234-567812345678',
            'collection_exercise_sid': '789',
            'form_type': 'calculated_summary',
            'eq_id': 'test',
        }
        answers = [
            {'answer_id': 'first-number-answer', 'value': 1},
            {'answer_id': 'second-number-answer', 'value': 2},
            {'answer_id': 'third-number-answer', 'value': 4},
            {'answer_id': 'fourth-number-answer', 'value': 6},
        ]
        current_location = Location('currency-total-playback-with-fourth')

        # When
        with self._application.test_request_context():
            view_context = build_view_context(block['type'], metadata, schema, ListStore(), AnswerStore(answers),
                                              block, current_location, form=None)

        # Then
        self.assertTrue('summary' in view_context)
        self.assertTrue('calculated_question' in view_context['summary'])
        self.assertEqual(view_context['summary']['title'],
                         'We calculate the total of currency values entered to be £13.00. Is this correct? (With Fourth)')

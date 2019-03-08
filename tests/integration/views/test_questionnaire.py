import simplejson as json
from flask import g
from mock import Mock
import pytest

from app.data_model.answer_store import AnswerStore
from app.data_model.questionnaire_store import QuestionnaireStore
from app.questionnaire.location import Location
from app.templating.view_context import build_view_context
from app.utilities.schema import load_schema_from_params
from app.views.questionnaire import get_page_title_for_location, _get_schema_context
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

    def tearDown(self):
        self._application_context.pop()

    def test_given_introduction_page_when_get_page_title_then_defaults_to_survey_title(self):
        # Given
        schema = load_schema_from_params('test', 'final_confirmation')

        # When
        page_title = get_page_title_for_location(schema, Location('introduction'), {}, AnswerStore())

        # Then
        self.assertEqual(page_title, 'Final confirmation to submit')

    def test_given_interstitial_page_when_get_page_title_then_group_title_and_survey_title(self):
        # Given
        schema = load_schema_from_params('test', 'interstitial_page')

        # When
        page_title = get_page_title_for_location(schema, Location('breakfast-interstitial'), {}, AnswerStore())

        # Then
        self.assertEqual(page_title, 'Favourite food - Interstitial Pages')

    def test_given_questionnaire_page_when_get_page_title_then_question_title_and_survey_title(self):
        # Given
        schema = load_schema_from_params('test', 'final_confirmation')

        # When
        page_title = get_page_title_for_location(schema, Location('breakfast'), {}, AnswerStore())

        # Then
        self.assertEqual(page_title, 'What is your favourite breakfast food - Final confirmation to submit')

    def test_given_questionnaire_page_when_get_page_title_with_titles_object(self):

        # Given
        schema = load_schema_from_params('test', 'titles')

        # When
        page_title = get_page_title_for_location(schema, Location('single-title-block'), {}, AnswerStore())

        # Then
        self.assertEqual(page_title, 'How are you feeling?? - Multiple Question Title Test')

    @pytest.mark.xfail
    def test_given_jinja_variable_question_title_when_get_page_title_then_replace_with_ellipsis(self):
        # Given
        schema = load_schema_from_params('test', 'relationship_household')

        # When
        page_title = get_page_title_for_location(schema, Location('household-relationships'), {}, AnswerStore())

        # Then
        self.assertEqual(page_title, 'How is … related to the people below? - Household relationship')

    def test_build_view_context_for_question(self):
        # Given
        g.schema = schema = load_schema_from_params('test', 'titles')
        block = g.schema.get_block('single-title-block')
        full_routing_path = [Location('single-title-block'),
                             Location('who-is-answer-block'),
                             Location('multiple-question-versions-block'),
                             Location('Summary')]
        current_location = Location('single-title-block')
        schema_context = _get_schema_context(full_routing_path, {}, {}, AnswerStore(), g.schema)

        # When
        with self._application.test_request_context():
            question_view_context = build_view_context('Question', {}, schema, AnswerStore(), schema_context, block,
                                                       current_location, form=None)

        # Then
        self.assertEqual(question_view_context['question_titles']['single-title-question'], 'How are you feeling??')

    def test_build_view_context_for_calculation_summary(self):
        # Given
        schema = load_schema_from_params('test', 'calculated_summary')
        block = schema.get_block('currency-total-playback')
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
        schema_context = {
            'answers': answers,
            'metadata': metadata
        }
        current_location = Location('currency-total-playback')

        # When
        with self._application.test_request_context():
            view_context = build_view_context(block['type'], metadata, schema, AnswerStore(answers),
                                              schema_context, block, current_location, form=None)

        # Then
        self.assertTrue('summary' in view_context)
        self.assertTrue('calculated_question' in view_context['summary'])
        self.assertEqual(view_context['summary']['title'],
                         'We calculate the total of currency values entered to be £13.00. Is this correct? (With Fourth)')

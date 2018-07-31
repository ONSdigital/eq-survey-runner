from flask import g
from mock import Mock
import simplejson as json

from app.data_model.answer_store import Answer, AnswerStore
from app.data_model.questionnaire_store import QuestionnaireStore
from app.questionnaire.location import Location
from app.templating.view_context import build_view_context
from app.utilities.schema import load_schema_from_params
from app.views.questionnaire import (
    remove_empty_household_members_from_answer_store,
    get_page_title_for_location,
    _get_schema_context
)

from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaire(IntegrationTestCase): # pylint: disable=too-many-public-methods
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

    def test_remove_empty_household_members_values_entered_are_stored(self):
        schema = load_schema_from_params('census', 'household')

        answered = [
            Answer(
                group_instance=0,
                answer_id='first-name',
                answer_instance=0,
                value='Joe'
            ), Answer(
                group_instance=0,
                answer_id='middle-names',
                answer_instance=0,
                value=''
            ), Answer(
                group_instance=0,
                answer_id='last-name',
                answer_instance=0,
                value='Bloggs'
            )
        ]

        unanswered = [
            Answer(
                group_instance=0,
                answer_id='first-name',
                answer_instance=1,
                value=''
            ), Answer(
                group_instance=0,
                answer_id='middle-names',
                answer_instance=1,
                value=''
            ), Answer(
                group_instance=0,
                answer_id='last-name',
                answer_instance=1,
                value=''
            )
        ]

        answers = []
        answers.extend(answered)
        answers.extend(unanswered)

        for answer in answers:
            self.question_store.answer_store.add_or_update(answer)

        remove_empty_household_members_from_answer_store(self.question_store.answer_store, schema)

        for answer in answered:
            self.assertIsNotNone(self.question_store.answer_store.find(answer))

        for answer in unanswered:
            self.assertIsNone(self.question_store.answer_store.find(answer))

    def test_remove_empty_household_members_partial_answers_are_stored(self):
        schema = load_schema_from_params('census', 'household')

        answered = [
            Answer(
                group_instance=0,
                answer_id='first-name',
                answer_instance=0,
                value='Joe'
            ), Answer(
                group_instance=0,
                answer_id='middle-names',
                answer_instance=0,
                value=''
            ), Answer(
                group_instance=0,
                answer_id='last-name',
                answer_instance=0,
                value='Bloggs'
            )
        ]

        partially_answered = [
            Answer(
                group_instance=0,
                answer_id='first-name',
                answer_instance=1,
                value=''
            ), Answer(
                group_instance=0,
                answer_id='middle-names',
                answer_instance=1,
                value=''
            ), Answer(
                group_instance=0,
                answer_id='last-name',
                answer_instance=1,
                value='Last name only'
            ), Answer(
                group_instance=0,
                answer_id='first-name',
                answer_instance=2,
                value='First name only'
            ), Answer(
                group_instance=0,
                answer_id='middle-names',
                answer_instance=2,
                value=''
            ), Answer(
                group_instance=0,
                answer_id='last-name',
                answer_instance=2,
                value=''
            )
        ]

        answers = []
        answers.extend(answered)
        answers.extend(partially_answered)

        for answer in answers:
            self.question_store.answer_store.add_or_update(answer)

        remove_empty_household_members_from_answer_store(self.question_store.answer_store, schema)

        for answer in answered:
            self.assertIsNotNone(self.question_store.answer_store.find(answer))

        for answer in partially_answered:
            self.assertIsNotNone(self.question_store.answer_store.find(answer))

    def test_remove_empty_household_members_middle_name_only_not_stored(self):
        schema = load_schema_from_params('census', 'household')

        unanswered = [
            Answer(
                group_instance=0,
                answer_id='first-name',
                answer_instance=0,
                value=''
            ), Answer(
                group_instance=0,
                answer_id='middle-names',
                answer_instance=0,
                value='should not be saved'
            ), Answer(
                group_instance=0,
                answer_id='last-name',
                answer_instance=0,
                value=''
            )
        ]

        for answer in unanswered:
            self.question_store.answer_store.add_or_update(answer)

        remove_empty_household_members_from_answer_store(self.question_store.answer_store, schema)

        for answer in unanswered:
            self.assertIsNone(self.question_store.answer_store.find(answer))

    def test_given_introduction_page_when_get_page_title_then_defaults_to_survey_title(self):
        # Given
        schema = load_schema_from_params('test', 'final_confirmation')

        # When
        page_title = get_page_title_for_location(schema, Location('final-confirmation', 0, 'introduction'), {})

        # Then
        self.assertEqual(page_title, 'Final confirmation to submit')

    def test_given_interstitial_page_when_get_page_title_then_group_title_and_survey_title(self):
        # Given
        schema = load_schema_from_params('test', 'interstitial_page')

        # When
        page_title = get_page_title_for_location(schema, Location('favourite-foods', 0, 'breakfast-interstitial'), {})

        # Then
        self.assertEqual(page_title, 'Favourite food - Interstitial Pages')

    def test_given_questionnaire_page_when_get_page_title_then_question_title_and_survey_title(self):
        # Given
        schema = load_schema_from_params('test', 'final_confirmation')

        # When
        page_title = get_page_title_for_location(schema, Location('final-confirmation', 0, 'breakfast'), {})

        # Then
        self.assertEqual(page_title, 'What is your favourite breakfast food - Final confirmation to submit')

    def test_given_questionnaire_page_when_get_page_title_with_titles_object(self):
        context = {'question_titles': {'single-title-question': 'How are you feeling??'}}

        # Given
        schema = load_schema_from_params('test', 'titles')

        # When
        page_title = get_page_title_for_location(schema, Location('group', 0, 'single-title-block'), context)

        # Then
        self.assertEqual(page_title, 'How are you feeling?? - Multiple Question Title Test')

    def test_given_jinja_variable_question_title_when_get_page_title_then_replace_with_ellipsis(self):
        # Given
        schema = load_schema_from_params('census', 'household')

        # When
        page_title = get_page_title_for_location(schema, Location('who-lives-here-relationship', 0, 'household-relationships'), {})

        # Then
        self.assertEqual(page_title, 'How is … related to the people below? - 2017 Census Test')

    def test_build_view_context_for_question(self):
        # Given
        g.schema = schema = load_schema_from_params('test', 'titles')
        block = g.schema.get_block('single-title-block')
        full_routing_path = [Location('group', 0, 'single-title-block'),
                             Location('group', 0, 'who-is-answer-block'),
                             Location('group', 0, 'multiple-question-versions-block'),
                             Location('group', 0, 'Summary')]
        schema_context = _get_schema_context(full_routing_path, 0, {}, AnswerStore(), schema)
        current_location = Location('group', 0, 'single-title-block')

        # When
        with self._application.test_request_context():
            question_view_context = build_view_context('Question', {}, schema, AnswerStore(), schema_context, block,
                                                       current_location, form=None)

        # Then
        self.assertEqual(question_view_context['question_titles']['single-title-question'], 'How are you feeling??')

    def test_remove_completed_by_group_and_block(self):
        for i in range(10):
            self.question_store.completed_blocks.append(Location('group1', i, 'block1'))

        self.question_store.completed_blocks.append(Location('group2', 0, 'block2'))

        self.question_store.remove_completed_blocks(group_id='group1', block_id='block1')

        self.assertEqual(len(self.question_store.completed_blocks), 1)
        self.assertEqual(self.question_store.completed_blocks[0], Location('group2', 0, 'block2'))

    def test_remove_completed_by_group_and_block_does_not_error_if_no_matching_blocks(self):
        for i in range(10):
            self.question_store.completed_blocks.append(Location('group1', i, 'block1'))

        self.question_store.completed_blocks.append(Location('group2', 0, 'block2'))

        self.question_store.remove_completed_blocks(group_id='group1', block_id='block2')
        self.question_store.remove_completed_blocks(group_id='group2', block_id='block1')

        # no exception equates to passed

from flask import g
from mock import Mock, patch
import simplejson as json

from app.data_model.answer_store import Answer, AnswerStore
from app.data_model.questionnaire_store import QuestionnaireStore
from app.questionnaire.location import Location
from app.templating.view_context import build_view_context
from app.utilities.schema import load_schema_from_params
from app.views.questionnaire import update_questionnaire_store_with_answer_data, \
    update_questionnaire_store_with_form_data, remove_empty_household_members_from_answer_store, \
    get_page_title_for_location, _get_schema_context

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

    def test_update_questionnaire_store_with_form_data(self):

        schema = load_schema_from_params('test', '0112')

        location = Location('rsi', 0, 'total-retail-turnover')

        form_data = {
            'total-retail-turnover-answer': '1000',
        }

        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(self.question_store, location, form_data, schema)

        self.assertEqual(self.question_store.completed_blocks, [location])

        self.assertIn({
            'group_instance': 0,
            'answer_id': 'total-retail-turnover-answer',
            'answer_instance': 0,
            'value': '1000'
        }, self.question_store.answer_store.answers)

    def test_update_questionnaire_store_with_default_value(self):

        schema = load_schema_from_params('test', 'default')

        location = Location('group', 0, 'number-question')

        # No answer given so will use schema defined default
        form_data = {
            'answer': None
        }

        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(self.question_store, location, form_data, schema)

        self.assertEqual(self.question_store.completed_blocks, [location])

        self.assertIn({
            'group_instance': 0,
            'answer_id': 'answer',
            'answer_instance': 0,
            'value': 0
        }, self.question_store.answer_store.answers)

    def test_update_questionnaire_store_with_answer_data(self):
        schema = load_schema_from_params('census', 'household')

        location = Location('who-lives-here', 0, 'household-composition')

        answers = [
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
            ), Answer(
                group_instance=0,
                answer_id='first-name',
                answer_instance=1,
                value='Bob'
            ), Answer(
                group_instance=0,
                answer_id='middle-names',
                answer_instance=1,
                value=''
            ), Answer(
                group_instance=0,
                answer_id='last-name',
                answer_instance=1,
                value='Seymour'
            )
        ]

        with self._application.test_request_context():
            update_questionnaire_store_with_answer_data(self.question_store, location, answers, schema)

        self.assertEqual(self.question_store.completed_blocks, [location])

        for answer in answers:
            self.assertIn(answer.__dict__, self.question_store.answer_store.answers)

    def test_remove_empty_household_members_from_answer_store(self):
        schema = load_schema_from_params('census', 'household')

        answers = [
            Answer(
                group_instance=0,
                answer_id='first-name',
                answer_instance=0,
                value=''
            ), Answer(
                group_instance=0,
                answer_id='middle-names',
                answer_instance=0,
                value=''
            ), Answer(
                group_instance=0,
                answer_id='last-name',
                answer_instance=0,
                value=''
            ), Answer(
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

        for answer in answers:
            self.question_store.answer_store.add_or_update(answer)

        remove_empty_household_members_from_answer_store(self.question_store.answer_store, schema)

        for answer in answers:
            self.assertIsNone(self.question_store.answer_store.find(answer))

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

    def test_updating_questionnaire_store_removes_completed_block_for_min_dependencies(self):

        schema = load_schema_from_params('test', 'dependencies_min_value')

        min_answer_location = Location('group', 0, 'min-block')
        dependent_location = Location('group', 0, 'dependent-block')

        min_answer_data = {
            'min-answer': '10',
        }

        dependent_data = {
            'dependent-1': '10',
        }

        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(self.question_store, min_answer_location, min_answer_data, schema)

        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(self.question_store, dependent_location, dependent_data, schema)

        self.assertIn(min_answer_location, self.question_store.completed_blocks)
        self.assertIn(dependent_location, self.question_store.completed_blocks)

        min_answer_data = {
            'min-answer': '9',
        }

        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(self.question_store, min_answer_location, min_answer_data, schema)

        self.assertNotIn(dependent_location, self.question_store.completed_blocks)

    def test_updating_questionnaire_store_removes_completed_block_for_max_dependencies(self):

        schema = load_schema_from_params('test', 'dependencies_max_value')

        max_answer_location = Location('group', 0, 'max-block')
        dependent_location = Location('group', 0, 'dependent-block')

        max_answer_data = {
            'max-answer': '10',
        }

        dependent_data = {
            'dependent-1': '10',
        }

        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(self.question_store, max_answer_location, max_answer_data, schema)

        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(self.question_store, dependent_location, dependent_data, schema)

        self.assertIn(max_answer_location, self.question_store.completed_blocks)
        self.assertIn(dependent_location, self.question_store.completed_blocks)

        max_answer_data = {
            'max-answer': '11',
        }

        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(self.question_store, max_answer_location, max_answer_data, schema)

        self.assertNotIn(dependent_location, self.question_store.completed_blocks)

    def test_updating_questionnaire_store_removes_completed_block_for_calculation_dependencies(self):

        schema = load_schema_from_params('test', 'dependencies_calculation')

        calculation_answer_location = Location('group', 0, 'total-block')
        dependent_location = Location('group', 0, 'breakdown-block')

        calculation_answer_data = {
            'total-answer': '100',
        }

        dependent_data = {
            'breakdown-1': '10',
            'breakdown-2': '20',
            'breakdown-3': '30',
            'breakdown-4': '40'
        }

        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(self.question_store, calculation_answer_location, calculation_answer_data, schema)

        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(self.question_store, dependent_location, dependent_data, schema)

        self.assertIn(calculation_answer_location, self.question_store.completed_blocks)
        self.assertIn(dependent_location, self.question_store.completed_blocks)

        calculation_answer_data = {
            'total-answer': '99',
        }

        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(self.question_store, calculation_answer_location, calculation_answer_data, schema)

        self.assertNotIn(dependent_location, self.question_store.completed_blocks)

    def test_updating_questionnaire_store_specific_group(self):
        schema = load_schema_from_params('test', 'repeating_household_routing')
        answers = [
            Answer(
                group_instance=0,
                answer_id='first-name',
                answer_instance=0,
                value='Joe'
            ), Answer(
                group_instance=0,
                answer_id='last-name',
                answer_instance=0,
                value='Bloggs'
            ), Answer(
                group_instance=0,
                answer_id='date-of-birth-answer',
                answer_instance=0,
                value='2016-03-12'
            ), Answer(
                group_instance=1,
                answer_id='date-of-birth-answer',
                answer_instance=0,
                value='2018-01-01'
            )
        ]

        for answer in answers:
            self.question_store.answer_store.add_or_update(answer)

        answer_form_data = {'date-of-birth-answer': None}
        location = Location('household-member-group', 1, 'date-of-birth')
        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(
                self.question_store, location, answer_form_data, schema)

        self.assertIsNone(self.question_store.answer_store.find(answers[3]))
        for answer in answers[:2]:
            self.assertIsNotNone(self.question_store.answer_store.find(answer))

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

    def test_answer_non_repeating_dependency_repeating_validate_all_of_block_and_group_removed(self):
        """ load a schema with a non repeating independent answer and a repeating one that depends on it
        validate that when the independent variable is set a call is made to remove all instances of
        the dependant variables
        """
        # Given
        schema = load_schema_from_params('test', 'titles_repeating_non_repeating_dependency')
        colour_answer_location = Location('colour-group', 0, 'favourite-colour')
        colour_answer = {'fav-colour-answer': 'blue'}

        # When
        with self._application.test_request_context():
            with patch('app.data_model.questionnaire_store.QuestionnaireStore.remove_completed_blocks') as patch_remove:
                update_questionnaire_store_with_form_data(self.question_store, colour_answer_location, colour_answer, schema)

        # Then
        patch_remove.assert_called_with(group_id='repeating-group', block_id='repeating-block-3')

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

class TestQuestionnaireLanguage(IntegrationTestCase):
    """ Tests that the language selection from tokens works """
    def test_load_cy_survey(self):
        # When: load a cy survey
        self.launchSurvey('test', 'language', language_code='cy')
        # Then: welsh
        self.assertInPage('Holiadur Cymraeg')

    def test_load_non_existant_lang_fallback(self):
        # When: load a hindi survey
        self.launchSurvey('test', 'language', language_code='hi')
        # Then: Falls back to english
        self.assertInPage('English Questionnaire')

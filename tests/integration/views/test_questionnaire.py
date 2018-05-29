from flask import g
from mock import Mock
import simplejson as json

from app.data_model.answer_store import Answer
from app.data_model.questionnaire_store import QuestionnaireStore
from app.questionnaire.location import Location
from app.utilities.schema import load_schema_from_params
from app.views.questionnaire import update_questionnaire_store_with_answer_data, \
    update_questionnaire_store_with_form_data, remove_empty_household_members_from_answer_store, \
    get_page_title_for_location

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

    def test_update_questionnaire_store_with_form_data(self):

        g.schema = load_schema_from_params('test', '0112')

        location = Location('rsi', 0, 'total-retail-turnover')

        form_data = {
            'total-retail-turnover-answer': '1000',
        }

        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(self.question_store, location, form_data)

        self.assertEqual(self.question_store.completed_blocks, [location])

        self.assertIn({
            'group_instance': 0,
            'answer_id': 'total-retail-turnover-answer',
            'answer_instance': 0,
            'value': '1000',
            'group_id': 'rsi',
            'block_id': 'total-retail-turnover'
        }, self.question_store.answer_store.answers)

    def test_update_questionnaire_store_with_default_value(self):

        g.schema = load_schema_from_params('test', 'default')

        location = Location('group', 0, 'number-question')

        # No answer given so will use schema defined default
        form_data = {
            'answer': None
        }

        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(self.question_store, location, form_data)

        self.assertEqual(self.question_store.completed_blocks, [location])

        self.assertIn({
            'group_instance': 0,
            'answer_id': 'answer',
            'answer_instance': 0,
            'value': 0,
            'group_id': 'group',
            'block_id': 'number-question'
        }, self.question_store.answer_store.answers)

    def test_update_questionnaire_store_with_date_form_data(self):

        g.schema = load_schema_from_params('test', 'dates')

        location = Location('dates', 0, 'date-block')

        form_data = {
            'single-date-answer': {'day': '12', 'month': '03', 'year': '2016'},
            'month-year-answer': {'month': '11', 'year': '2014'},
        }

        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(self.question_store, location, form_data)

        self.assertEqual(self.question_store.completed_blocks, [location])

        self.assertIn({
            'group_instance': 0,
            'answer_id': 'single-date-answer',
            'answer_instance': 0,
            'value': '2016-03-12',
            'group_id': 'dates',
            'block_id': 'date-block'
        }, self.question_store.answer_store.answers)

        self.assertIn({
            'group_instance': 0,
            'answer_id': 'month-year-answer',
            'answer_instance': 0,
            'value': '2014-11',
            'group_id': 'dates',
            'block_id': 'date-block'
        }, self.question_store.answer_store.answers)

    def test_update_questionnaire_store_with_empty_day_month_year_date(self):

        g.schema = load_schema_from_params('test', 'dates')

        location = Location('dates', 0, 'date-block')

        form_data = {
            'non-mandatory-date-answer': {'day': '', 'month': '', 'year': ''},
        }

        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(self.question_store, location, form_data)

        self.assertEqual([], self.question_store.answer_store.answers)

    def test_update_questionnaire_store_with_empty_month_year_date(self):

        g.schema = load_schema_from_params('test', 'dates')

        location = Location('dates', 0, 'date-block')

        form_data = {
            'month-year-answer': {'month': '', 'year': ''},
        }

        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(self.question_store, location, form_data)

        self.assertEqual([], self.question_store.answer_store.answers)

    def test_update_questionnaire_store_with_answer_data(self):
        g.schema = load_schema_from_params('census', 'household')

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
            update_questionnaire_store_with_answer_data(self.question_store, location, answers)

        self.assertEqual(self.question_store.completed_blocks, [location])

        for answer in answers:
            self.assertIn(answer.__dict__, self.question_store.answer_store.answers)

    def test_remove_empty_household_members_from_answer_store(self):
        g.schema = load_schema_from_params('census', 'household')

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

        remove_empty_household_members_from_answer_store(self.question_store.answer_store)

        for answer in answers:
            self.assertIsNone(self.question_store.answer_store.find(answer))

    def test_remove_empty_household_members_values_entered_are_stored(self):
        g.schema = load_schema_from_params('census', 'household')

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

        remove_empty_household_members_from_answer_store(self.question_store.answer_store)

        for answer in answered:
            self.assertIsNotNone(self.question_store.answer_store.find(answer))

        for answer in unanswered:
            self.assertIsNone(self.question_store.answer_store.find(answer))

    def test_remove_empty_household_members_partial_answers_are_stored(self):
        g.schema = load_schema_from_params('census', 'household')

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

        remove_empty_household_members_from_answer_store(self.question_store.answer_store)

        for answer in answered:
            self.assertIsNotNone(self.question_store.answer_store.find(answer))

        for answer in partially_answered:
            self.assertIsNotNone(self.question_store.answer_store.find(answer))

    def test_remove_empty_household_members_middle_name_only_not_stored(self):
        g.schema = load_schema_from_params('census', 'household')

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

        remove_empty_household_members_from_answer_store(self.question_store.answer_store)

        for answer in unanswered:
            self.assertIsNone(self.question_store.answer_store.find(answer))

    def test_given_introduction_page_when_get_page_title_then_defaults_to_survey_title(self):
        # Given
        schema = load_schema_from_params('test', 'final_confirmation')

        # When
        page_title = get_page_title_for_location(schema, Location('final-confirmation', 0, 'introduction'))

        # Then
        self.assertEqual(page_title, 'Final confirmation to submit')

    def test_given_interstitial_page_when_get_page_title_then_group_title_and_survey_title(self):
        # Given
        schema = load_schema_from_params('test', 'interstitial_page')

        # When
        page_title = get_page_title_for_location(schema, Location('favourite-foods', 0, 'breakfast-interstitial'))

        # Then
        self.assertEqual(page_title, 'Favourite food - Interstitial Pages')

    def test_given_questionnaire_page_when_get_page_title_then_question_title_and_survey_title(self):
        # Given
        schema = load_schema_from_params('test', 'final_confirmation')

        # When
        page_title = get_page_title_for_location(schema, Location('final-confirmation', 0, 'breakfast'))

        # Then
        self.assertEqual(page_title, 'What is your favourite breakfast food - Final confirmation to submit')

    def test_given_jinja_variable_question_title_when_get_page_title_then_replace_with_ellipsis(self):
        # Given
        schema = load_schema_from_params('census', 'household')

        # When
        page_title = get_page_title_for_location(schema, Location('who-lives-here-relationship', 0, 'household-relationships'))

        # Then
        self.assertEqual(page_title, 'How is … related to the people below? - 2017 Census Test')

    def test_updating_questionnaire_store_removes_completed_block_for_min_dependencies(self):

        g.schema = load_schema_from_params('test', 'dependencies_min_value')

        min_answer_location = Location('group', 0, 'min-block')
        dependent_location = Location('group', 0, 'dependent-block')

        min_answer_data = {
            'min-answer': '10',
        }

        dependent_data = {
            'dependent-1': '10',
        }

        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(self.question_store, min_answer_location, min_answer_data)

        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(self.question_store, dependent_location, dependent_data)

        self.assertIn(min_answer_location, self.question_store.completed_blocks)
        self.assertIn(dependent_location, self.question_store.completed_blocks)

        min_answer_data = {
            'min-answer': '9',
        }

        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(self.question_store, min_answer_location, min_answer_data)

        self.assertNotIn(dependent_location, self.question_store.completed_blocks)

    def test_updating_questionnaire_store_removes_completed_block_for_max_dependencies(self):

        g.schema = load_schema_from_params('test', 'dependencies_max_value')

        max_answer_location = Location('group', 0, 'max-block')
        dependent_location = Location('group', 0, 'dependent-block')

        max_answer_data = {
            'max-answer': '10',
        }

        dependent_data = {
            'dependent-1': '10',
        }

        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(self.question_store, max_answer_location, max_answer_data)

        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(self.question_store, dependent_location, dependent_data)

        self.assertIn(max_answer_location, self.question_store.completed_blocks)
        self.assertIn(dependent_location, self.question_store.completed_blocks)

        max_answer_data = {
            'max-answer': '11',
        }

        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(self.question_store, max_answer_location, max_answer_data)

        self.assertNotIn(dependent_location, self.question_store.completed_blocks)

    def test_updating_questionnaire_store_removes_completed_block_for_calculation_dependencies(self):

        g.schema = load_schema_from_params('test', 'dependencies_calculation')

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
            update_questionnaire_store_with_form_data(self.question_store, calculation_answer_location, calculation_answer_data)

        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(self.question_store, dependent_location, dependent_data)

        self.assertIn(calculation_answer_location, self.question_store.completed_blocks)
        self.assertIn(dependent_location, self.question_store.completed_blocks)

        calculation_answer_data = {
            'total-answer': '99',
        }

        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(self.question_store, calculation_answer_location, calculation_answer_data)

        self.assertNotIn(dependent_location, self.question_store.completed_blocks)

    def test_updating_questionnaire_store_specific_group(self):
        g.schema = load_schema_from_params('test',
                                           'repeating_household_routing')
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

        answer_form_data = {'date-of-birth-answer': {}}
        location = Location('household-member-group', 1, 'date-of-birth')
        with self._application.test_request_context():
            update_questionnaire_store_with_form_data(
                self.question_store, location, answer_form_data)

        self.assertIsNone(self.question_store.answer_store.find(answers[3]))
        for answer in answers[:2]:
            self.assertIsNotNone(self.question_store.answer_store.find(answer))

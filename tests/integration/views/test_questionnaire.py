import json

from flask import g
from mock import Mock

from app.data_model.answer_store import Answer
from app.data_model.questionnaire_store import QuestionnaireStore
from app.questionnaire.location import Location
from app.utilities.schema import load_schema_file
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
        storage.get_user_data = Mock(return_value=json.dumps(data, default=lambda o: o.__dict__))

        self.question_store = QuestionnaireStore(storage)

    def tearDown(self):
        self._application_context.pop()

    def test_update_questionnaire_store_with_form_data(self):

        g.schema_json = load_schema_file("1_0112.json")

        location = Location("rsi", 0, "total-retail-turnover")

        form_data = {
            'total-retail-turnover-answer': "1000",
        }

        update_questionnaire_store_with_form_data(self.question_store, location, form_data)

        self.assertEqual(self.question_store.completed_blocks, [location])

        self.assertIn({
            'group_id': 'rsi',
            'group_instance': 0,
            'block_id': 'total-retail-turnover',
            'answer_id': 'total-retail-turnover-answer',
            'answer_instance': 0,
            'value': '1000',
        }, self.question_store.answer_store.answers)

    def test_update_questionnaire_store_with_date_form_data(self):

        g.schema_json = load_schema_file("test_dates.json")

        location = Location("dates", 0, "date-block")

        form_data = {
            'single-date-answer': {'day': '12', 'month': '03', 'year': '2016'},
            'month-year-answer': {'month': '11', 'year': '2014'},
        }

        update_questionnaire_store_with_form_data(self.question_store, location, form_data)

        self.assertEqual(self.question_store.completed_blocks, [location])

        self.assertIn({
            'group_id': 'dates',
            'group_instance': 0,
            'block_id': 'date-block',
            'answer_id': 'single-date-answer',
            'answer_instance': 0,
            'value': '12/03/2016',
        }, self.question_store.answer_store.answers)

        self.assertIn({
            'group_id': 'dates',
            'group_instance': 0,
            'block_id': 'date-block',
            'answer_id': 'month-year-answer',
            'answer_instance': 0,
            'value': '11/2014',
        }, self.question_store.answer_store.answers)

    def test_update_questionnaire_store_with_empty_day_month_year_date(self):

        g.schema_json = load_schema_file("test_dates.json")

        location = Location("dates", 0, "date-block")

        form_data = {
            'non-mandatory-date-answer': {'day': '', 'month': '', 'year': ''},
        }

        update_questionnaire_store_with_form_data(self.question_store, location, form_data)
        self.assertEqual([], self.question_store.answer_store.answers)

    def test_update_questionnaire_store_with_empty_month_year_date(self):

        g.schema_json = load_schema_file("test_dates.json")

        location = Location("dates", 0, "date-block")

        form_data = {
            'month-year-answer': {'month': '', 'year': ''},
        }

        update_questionnaire_store_with_form_data(self.question_store, location, form_data)
        self.assertEqual([], self.question_store.answer_store.answers)

    def test_update_questionnaire_store_with_answer_data(self):
        g.schema_json = load_schema_file("census_household.json")

        location = Location('who-lives-here', 0, 'household-composition')

        answers = [
            Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='first-name',
                answer_instance=0,
                value='Joe'
            ), Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='middle-names',
                answer_instance=0,
                value=''
            ), Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='last-name',
                answer_instance=0,
                value='Bloggs'
            ), Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='first-name',
                answer_instance=1,
                value='Bob'
            ), Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='middle-names',
                answer_instance=1,
                value=''
            ), Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='last-name',
                answer_instance=1,
                value='Seymour'
            )
        ]

        update_questionnaire_store_with_answer_data(self.question_store, location, answers)

        self.assertEqual(self.question_store.completed_blocks, [location])

        for answer in answers:
            self.assertIn(answer.__dict__, self.question_store.answer_store.answers)

    def test_remove_empty_household_members_from_answer_store(self):
        g.schema_json = load_schema_file("census_household.json")

        answers = [
            Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='first-name',
                answer_instance=0,
                value=''
            ), Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='middle-names',
                answer_instance=0,
                value=''
            ), Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='last-name',
                answer_instance=0,
                value=''
            ), Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='first-name',
                answer_instance=1,
                value=''
            ), Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='middle-names',
                answer_instance=1,
                value=''
            ), Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='last-name',
                answer_instance=1,
                value=''
            )
        ]

        for answer in answers:
            self.question_store.answer_store.add_or_update(answer)

        remove_empty_household_members_from_answer_store(self.question_store.answer_store, 'who-lives-here')

        for answer in answers:
            self.assertFalse(self.question_store.answer_store.exists(answer))

    def test_remove_empty_household_members_values_entered_are_stored(self):
        g.schema_json = load_schema_file("census_household.json")

        answered = [
            Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='first-name',
                answer_instance=0,
                value='Joe'
            ), Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='middle-names',
                answer_instance=0,
                value=''
            ), Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='last-name',
                answer_instance=0,
                value='Bloggs'
            )
        ]

        unanswered = [
            Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='first-name',
                answer_instance=1,
                value=''
            ), Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='middle-names',
                answer_instance=1,
                value=''
            ), Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
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

        remove_empty_household_members_from_answer_store(self.question_store.answer_store, 'who-lives-here')

        for answer in answered:
            self.assertTrue(self.question_store.answer_store.exists(answer))

        for answer in unanswered:
            self.assertFalse(self.question_store.answer_store.exists(answer))

    def test_remove_empty_household_members_partial_answers_are_stored(self):
        g.schema_json = load_schema_file("census_household.json")

        answered = [
            Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='first-name',
                answer_instance=0,
                value='Joe'
            ), Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='middle-names',
                answer_instance=0,
                value=''
            ), Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='last-name',
                answer_instance=0,
                value='Bloggs'
            )
        ]

        partially_answered = [
            Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='first-name',
                answer_instance=1,
                value=''
            ), Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='middle-names',
                answer_instance=1,
                value=''
            ), Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='last-name',
                answer_instance=1,
                value='Last name only'
            ), Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='first-name',
                answer_instance=2,
                value='First name only'
            ), Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='middle-names',
                answer_instance=2,
                value=''
            ), Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
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

        remove_empty_household_members_from_answer_store(self.question_store.answer_store, 'who-lives-here')

        for answer in answered:
            self.assertTrue(self.question_store.answer_store.exists(answer))

        for answer in partially_answered:
            self.assertTrue(self.question_store.answer_store.exists(answer))

    def test_remove_empty_household_members_middle_name_only_not_stored(self):
        g.schema_json = load_schema_file("census_household.json")

        unanswered = [
            Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='first-name',
                answer_instance=0,
                value=''
            ), Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='middle-names',
                answer_instance=0,
                value='should not be saved'
            ), Answer(
                group_id='who-lives-here',
                group_instance=0,
                block_id='household-composition',
                answer_id='last-name',
                answer_instance=0,
                value=''
            )
        ]

        for answer in unanswered:
            self.question_store.answer_store.add_or_update(answer)

        remove_empty_household_members_from_answer_store(self.question_store.answer_store, 'who-lives-here')

        for answer in unanswered:
            self.assertFalse(self.question_store.answer_store.exists(answer))

    def test_given_introduction_page_when_get_page_title_then_defaults_to_survey_title(self):
        # Given
        g.schema_json = load_schema_file("test_final_confirmation.json")

        # When
        page_title = get_page_title_for_location(g.schema_json, Location('final-confirmation', 0, 'introduction'))

        # Then
        self.assertEqual(page_title, 'Final confirmation to submit')

    def test_given_interstitial_page_when_get_page_title_then_group_title_and_survey_title(self):
        # Given
        g.schema_json = load_schema_file("test_interstitial_page.json")

        # When
        page_title = get_page_title_for_location(g.schema_json, Location('favourite-foods', 0, 'breakfast-interstitial'))

        # Then
        self.assertEqual(page_title, 'Favourite food - Interstitial Pages')

    def test_given_questionnaire_page_when_get_page_title_then_question_title_and_survey_title(self):
        # Given
        g.schema_json = load_schema_file("test_final_confirmation.json")

        # When
        page_title = get_page_title_for_location(g.schema_json, Location('final-confirmation', 0, 'breakfast'))

        # Then
        self.assertEqual(page_title, 'What is your favourite breakfast food - Final confirmation to submit')

    def test_given_jinja_variable_question_title_when_get_page_title_then_replace_with_ellipsis(self):
        # Given
        g.schema_json = load_schema_file("census_household.json")

        # When
        page_title = get_page_title_for_location(g.schema_json, Location('who-lives-here-relationship', 0, 'household-relationships'))

        # Then
        self.assertEqual(page_title, 'How is … related to the people below? - 2017 Census Test')

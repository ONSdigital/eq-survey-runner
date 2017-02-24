import json
import unittest

from mock import Mock

from app import create_app
from app.data_model.answer_store import Answer
from app.data_model.questionnaire_store import QuestionnaireStore
from app.schema_loader.schema_loader import load_schema_file
from app.questionnaire.location import Location
from app.views.questionnaire import update_questionnaire_store_with_answer_data, update_questionnaire_store_with_form_data, remove_empty_household_members_from_answer_store

from flask import g


class TestQuestionnaireView(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SERVER_NAME'] = "test"
        self.app_context = self.app.app_context()
        self.app_context.push()

        storage = Mock()
        data = {
            'METADATA': 'test',
            'ANSWERS': [],
            'COMPLETED_BLOCKS': []
        }
        storage.get_user_data = Mock(return_value=json.dumps(data, default=lambda o: o.__dict__))

        self.question_store = QuestionnaireStore(storage)

    def tearDown(self):
        self.app_context.pop()

    def test_update_questionnaire_store_with_form_data(self):

        g.schema_json = load_schema_file("1_0112.json")

        location = Location("rsi", 0, "total-retail-turnover")

        form_data = {
            'total-retail-turnover-answer': "1000",
        }

        update_questionnaire_store_with_form_data(self.question_store, location, form_data)

        self.assertEquals(self.question_store.completed_blocks, [location])

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

        self.assertEquals(self.question_store.completed_blocks, [location])

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

        self.assertEquals(self.question_store.completed_blocks, [location])

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
            ),  Answer(
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

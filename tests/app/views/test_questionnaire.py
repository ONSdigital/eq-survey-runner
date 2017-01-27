import json
import unittest

from mock import Mock

from app import create_app
from app.data_model.answer_store import Answer
from app.data_model.questionnaire_store import QuestionnaireStore
from app.schema_loader.schema_loader import load_schema_file
from app.questionnaire.location import Location
from app.views.questionnaire import update_questionnaire_store_with_answer_data, update_questionnaire_store_with_form_data

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

        location = Location("a23d36db-6b07-4ce0-94b2-a843369511e3", 0, "date-block")

        form_data = {
            'single-date-answer': {'day': '12', 'month': '03', 'year': '2016'},
            'month-year-answer': {'month': '11', 'year': '2014'},
        }

        update_questionnaire_store_with_form_data(self.question_store, location, form_data)

        self.assertEquals(self.question_store.completed_blocks, [location])

        self.assertIn({
            'group_id': 'a23d36db-6b07-4ce0-94b2-a843369511e3',
            'group_instance': 0,
            'block_id': 'date-block',
            'answer_id': 'single-date-answer',
            'answer_instance': 0,
            'value': '12/03/2016',
        }, self.question_store.answer_store.answers)

        self.assertIn({
            'group_id': 'a23d36db-6b07-4ce0-94b2-a843369511e3',
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

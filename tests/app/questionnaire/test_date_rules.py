from datetime import datetime

from app.data_model.answer_store import AnswerStore, Answer
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.rules import evaluate_date_rule, evaluate_goto
from tests.app.app_context_test_case import AppContextTestCase


def get_schema_mock():
    schema = QuestionnaireSchema({})
    return schema


class TestDateRules(AppContextTestCase):

    def test_evaluate_date_rule_equals_with_value_now(self):

        when = {
            'id': 'date-answer',
            'condition': 'equals',
            'date_comparison': {
                'value': 'now'
            }
        }

        answer_value = datetime.utcnow().strftime('%Y-%m-%d')
        result = evaluate_date_rule(when, None, get_schema_mock(), None, answer_value)
        self.assertTrue(result)

        answer_value = '2000-01-01'
        result = evaluate_date_rule(when, None, get_schema_mock(), None, answer_value)
        self.assertFalse(result)

    def test_evaluate_date_rule_equals_with_with_offset(self):

        when = {
            'id': 'date-answer',
            'condition': 'equals',
            'date_comparison': {
                'value': '2019-03-31',
                'offset_by': {
                    'days': 1,
                    'months': 1,
                    'years': 1
                }
            }
        }

        answer_value = '2020-05-01'
        result = evaluate_date_rule(when, None, get_schema_mock(), None, answer_value)
        self.assertTrue(result)

        when = {
            'id': 'date-answer',
            'condition': 'equals',
            'date_comparison': {
                'value': '2021-04-01',
                'offset_by': {
                    'days': -1,
                    'months': -1,
                    'years': -1
                }
            }
        }

        answer_value = '2020-02-29'
        result = evaluate_date_rule(when, None, get_schema_mock(), None, answer_value)
        self.assertTrue(result)

    def test_evaluate_date_rule_not_equals_with_value_year_month(self):

        when = {
            'id': 'date-answer',
            'condition': 'not equals',
            'date_comparison': {
                'value': '2018-01'
            }
        }

        answer_value = '2018-02'
        result = evaluate_date_rule(when, None, get_schema_mock(), None, answer_value)
        self.assertTrue(result)

        answer_value = '2018-01'
        result = evaluate_date_rule(when, None, get_schema_mock(), None, answer_value)
        self.assertFalse(result)

    def test_evaluate_date_rule_less_than_meta(self):

        metadata = {'return_by': '2016-06-12'}
        when = {
            'id': 'date-answer',
            'condition': 'less than',
            'date_comparison': {
                'meta': 'return_by'
            }
        }

        answer_value = '2016-06-11'
        result = evaluate_date_rule(when, None, get_schema_mock(), metadata, answer_value)
        self.assertTrue(result)

        answer_value = '2016-06-12'
        result = evaluate_date_rule(when, None, get_schema_mock(), metadata, answer_value)
        self.assertFalse(result)

    def test_evaluate_date_rule_greater_than_with_id(self):

        when = {
            'id': 'date-answer',
            'condition': 'greater than',
            'date_comparison': {
                'id': 'compare_date_answer'
            }
        }

        answer_store = AnswerStore({})
        answer_store.add_or_update(Answer(answer_id='compare_date_answer', value='2018-02-03'))

        answer_value = '2018-02-04'
        result = evaluate_date_rule(when, answer_store, get_schema_mock(), None, answer_value)
        self.assertTrue(result)

        answer_value = '2018-02-03'
        result = evaluate_date_rule(when, answer_store, get_schema_mock(), None, answer_value)
        self.assertFalse(result)

    def test_do_not_go_to_next_question_for_date_answer(self):

        goto_rule = {
            'id': 'next-question',
            'when': [{
                'id': 'date-answer',
                'condition': 'equals',
                'date_comparison': {
                    'value': '2018-01'
                }
            }]
        }

        answer_store = AnswerStore({})
        answer_store.add_or_update(Answer(answer_id='date_answer', value='2018-02-01'))

        self.assertFalse(evaluate_goto(goto_rule, get_schema_mock(), {}, answer_store, 0))

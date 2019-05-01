from unittest.mock import patch

from app.data_model.answer_store import AnswerStore, Answer
from app.questionnaire.location import Location
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.rules import evaluate_rule, evaluate_goto, \
    evaluate_skip_conditions, evaluate_when_rules
from tests.app.app_context_test_case import AppContextTestCase


def get_schema_mock():
    schema = QuestionnaireSchema({})
    return schema


class TestRules(AppContextTestCase):  # pylint: disable=too-many-public-methods

    def test_evaluate_rule_uses_single_value_from_list(self):
        when = {
            'value': 'singleAnswer',
            'condition': 'contains'
        }

        list_of_answers = ['singleAnswer']

        self.assertTrue(evaluate_rule(when, list_of_answers))

    def test_evaluate_rule_uses_multiple_values_in_list_returns_false(self):
        when = {
            'value': 'firstAnswer',
            'condition': 'equals'
        }

        list_of_answers = ['firstAnswer', 'secondAnswer']

        self.assertFalse(evaluate_rule(when, list_of_answers))

    def test_evaluate_rule_uses_boolean_value(self):
        when = {
            'value': False,
            'condition': 'equals'
        }

        self.assertTrue(evaluate_rule(when, False))

        when = {
            'value': True,
            'condition': 'not equals'
        }

        self.assertTrue(evaluate_rule(when, False))

    def test_evaluate_rule_set_should_be_true(self):
        when = {
            'condition': 'set'
        }

        self.assertTrue(evaluate_rule(when, ''))
        self.assertTrue(evaluate_rule(when, '0'))
        self.assertTrue(evaluate_rule(when, 'Yes'))
        self.assertTrue(evaluate_rule(when, 'No'))
        self.assertTrue(evaluate_rule(when, 0))
        self.assertTrue(evaluate_rule(when, 1))

    def test_evaluate_rule_set_should_be_false(self):
        when = {
            'condition': 'set'
        }

        self.assertFalse(evaluate_rule(when, None))

    def test_evaluate_rule_not_set_should_be_true(self):
        when = {
            'condition': 'not set'
        }

        self.assertTrue(evaluate_rule(when, None))

    def test_evaluate_rule_not_set_should_be_false(self):
        when = {
            'condition': 'not set'
        }

        self.assertFalse(evaluate_rule(when, ''))
        self.assertFalse(evaluate_rule(when, 'some text'))

    def test_evaluate_rule_not_set_on_empty_list_should_be_true(self):
        when = {
            'condition': 'not set'
        }

        self.assertTrue(evaluate_rule(when, []))

    def test_evaluate_rule_not_set_on_list_with_data_should_be_false(self):
        when = {
            'condition': 'not set'
        }

        self.assertFalse(evaluate_rule(when, ['123']))

    def test_evaluate_rule_set_on_list_with_data_should_be_true(self):
        when = {
            'condition': 'set'
        }

        self.assertTrue(evaluate_rule(when, ['123']))

    def test_evaluate_rule_set_on_empty_list_should_be_false(self):
        when = {
            'condition': 'set'
        }

        self.assertFalse(evaluate_rule(when, []))

    def test_evaluate_rule_equals_with_number(self):
        when = {
            'value': 0,
            'condition': 'equals'
        }

        self.assertFalse(evaluate_rule(when, 2))
        self.assertTrue(evaluate_rule(when, 0))

    def test_evaluate_rule_not_equals_with_number(self):
        when = {
            'value': 0,
            'condition': 'not equals'
        }

        self.assertTrue(evaluate_rule(when, 2))
        self.assertFalse(evaluate_rule(when, 0))

    def test_evaluate_rule_greater_than_or_equals_with_number(self):
        when = {
            'value': 4,
            'condition': 'greater than or equal to'
        }

        self.assertTrue(evaluate_rule(when, 4))
        self.assertTrue(evaluate_rule(when, 5))
        self.assertFalse(evaluate_rule(when, 3))
        self.assertFalse(evaluate_rule(when, None))

    def test_evaluate_rule_less_than_or_equals_with_number(self):
        when = {
            'value': 4,
            'condition': 'less than or equal to'
        }

        self.assertTrue(evaluate_rule(when, 4))
        self.assertTrue(evaluate_rule(when, 3))
        self.assertFalse(evaluate_rule(when, 5))
        self.assertFalse(evaluate_rule(when, None))

    def test_evaluate_rule_greater_than_with_number(self):
        when = {
            'value': 5,
            'condition': 'greater than'
        }

        self.assertTrue(evaluate_rule(when, 7))
        self.assertFalse(evaluate_rule(when, 5))
        self.assertFalse(evaluate_rule(when, 3))

    def test_evaluate_rule_less_than_with_number(self):
        when = {
            'value': 5,
            'condition': 'less than'
        }

        self.assertTrue(evaluate_rule(when, 3))
        self.assertFalse(evaluate_rule(when, 5))
        self.assertFalse(evaluate_rule(when, 7))

    def test_go_to_next_question_for_answer(self):
        # Given
        goto = {
            'id': 'next-question',
            'when': [
                {
                    'id': 'my_answer',
                    'condition': 'equals',
                    'value': 'Yes'
                }
            ]
        }
        answer_store = AnswerStore({})

        answer_store.add_or_update(Answer(answer_id='my_answer', value='Yes'))

        self.assertTrue(evaluate_goto(goto, get_schema_mock(), {}, answer_store))

    def test_do_not_go_to_next_question_for_answer(self):
        # Given
        goto_rule = {
            'id': 'next-question',
            'when': [
                {
                    'id': 'my_answer',
                    'condition': 'equals',
                    'value': 'Yes'
                }
            ]
        }
        answer_store = AnswerStore({})

        answer_store.add_or_update(Answer(answer_id='my_answer', value='No'))

        self.assertFalse(evaluate_goto(goto_rule, get_schema_mock(), {}, answer_store))

    def test_evaluate_goto_returns_true_when_answer_value_list_contains_match_value(self):

        goto = {
            'id': 'next-question',
            'when': [
                {
                    'id': 'my_answers',
                    'condition': 'contains',
                    'value': 'answer1'
                }
            ]
        }
        answer_store = AnswerStore({})
        answer_store.add_or_update(Answer(answer_id='my_answers', value=['answer1', 'answer2', 'answer3']))

        self.assertTrue(evaluate_goto(goto, get_schema_mock(), {}, answer_store))

    def test_evaluate_goto_returns_true_when_answer_value_list_not_contains_match_value(self):

        goto = {
            'id': 'next-question',
            'when': [
                {
                    'id': 'my_answers',
                    'condition': 'not contains',
                    'value': 'answer1'
                }
            ]
        }
        answer_store = AnswerStore({})
        answer_store.add_or_update(Answer(answer_id='my_answers', value=['answer2', 'answer3']))

        self.assertTrue(evaluate_goto(goto, get_schema_mock(), {}, answer_store, 0))

    def test_evaluate_goto_returns_true_when_answer_values_contains_any_match_values(self):

        goto = {
            'id': 'next-question',
            'when': [
                {
                    'id': 'my_answers',
                    'condition': 'contains any',
                    'value': ['answer1', 'answer2']
                }
            ]
        }
        answer_store = AnswerStore({})
        answer_store.add_or_update(Answer(answer_id='my_answers', value=['answer1', 'answer4']))

        self.assertTrue(evaluate_goto(goto, get_schema_mock(), {}, answer_store))

    def test_evaluate_goto_returns_true_when_answer_values_contains_all_match_values(self):

        goto = {
            'id': 'next-question',
            'when': [
                {
                    'id': 'my_answers',
                    'condition': 'contains all',
                    'value': ['answer1', 'answer2']
                }
            ]
        }
        answer_store = AnswerStore({})
        answer_store.add_or_update(Answer(answer_id='my_answers', value=['answer1', 'answer2', 'answer3']))

        self.assertTrue(evaluate_goto(goto, get_schema_mock(), {}, answer_store))

    def test_evaluate_goto_returns_true_when_answer_value_equals_any_match_values(self):

        goto = {
            'id': 'next-question',
            'when': [
                {
                    'id': 'my_answers',
                    'condition': 'equals any',
                    'values': ['answer1', 'answer2']
                }
            ]
        }
        answer_store = AnswerStore({})
        answer_store.add_or_update(Answer(answer_id='my_answers', value='answer2'))

        self.assertTrue(evaluate_goto(goto, get_schema_mock(), {}, answer_store))

    def test_evaluate_goto_returns_true_when_answer_value_not_equals_any_match_values(self):

        goto = {
            'id': 'next-question',
            'when': [
                {
                    'id': 'my_answers',
                    'condition': 'not equals any',
                    'values': ['answer1', 'answer2'],
                }
            ]
        }
        answer_store = AnswerStore({})
        answer_store.add_or_update(Answer(answer_id='my_answers', value='answer3'))

        self.assertTrue(evaluate_goto(goto, get_schema_mock(), {}, answer_store))

    def test_evaluate_skip_condition_returns_true_when_this_rule_true(self):
        # Given
        skip_conditions = [
            {
                'when': [
                    {
                        'id': 'this',
                        'condition': 'equals',
                        'value': 'value'
                    }
                ]
            },
            {
                'when': [
                    {
                        'id': 'that',
                        'condition': 'equals',
                        'value': 'other value'
                    }
                ]
            }
        ]
        answer_store = AnswerStore({})
        answer_store.add_or_update(Answer(answer_id='this', value='value'))

        # When
        condition = evaluate_skip_conditions(skip_conditions, get_schema_mock(), {}, answer_store)

        # Given
        self.assertTrue(condition)

    def test_evaluate_skip_condition_returns_true_when_that_rule_true(self):

        skip_conditions = [
            {
                'when': [
                    {
                        'id': 'this',
                        'condition': 'equals',
                        'value': 'value'
                    }
                ]
            },
            {
                'when': [
                    {
                        'id': 'that',
                        'condition': 'equals',
                        'value': 'other value'
                    }
                ]
            }
        ]
        answer_store = AnswerStore({})

        answer_store.add_or_update(Answer(answer_id='that', value='other value'))

        self.assertTrue(evaluate_skip_conditions(skip_conditions, get_schema_mock(), {}, answer_store))

    def test_evaluate_skip_condition_returns_true_when_more_than_one_rule_is_true(self):
        # Given
        skip_conditions = [
            {
                'when': [
                    {
                        'id': 'this',
                        'condition': 'equals',
                        'value': 'value'
                    }
                ]
            },
            {
                'when': [
                    {
                        'id': 'that',
                        'condition': 'equals',
                        'value': 'other value'
                    }
                ]
            }
        ]
        answer_store = AnswerStore({})
        answer_store.add_or_update(Answer(answer_id='this', value='value'))
        answer_store.add_or_update(Answer(answer_id='that', value='other value'))

        # When
        condition = evaluate_skip_conditions(skip_conditions, get_schema_mock(), {}, answer_store)

        # Then
        self.assertTrue(condition)

    def test_evaluate_skip_condition_returns_false_when_both_or_rules_false(self):
        # Given
        skip_conditions = [
            {
                'when': [
                    {
                        'id': 'this',
                        'condition': 'equals',
                        'value': 'value'
                    }
                ]
            },
            {
                'when': [
                    {
                        'id': 'that',
                        'condition': 'equals',
                        'value': 'other value'
                    }
                ]
            }
        ]
        answer_store = AnswerStore({})
        answer_store.add_or_update(Answer(answer_id='this', value='not correct'))
        answer_store.add_or_update(Answer(answer_id='that', value='not correct'))

        # When
        condition = evaluate_skip_conditions(skip_conditions, get_schema_mock(), {}, answer_store)

        # Then
        self.assertFalse(condition)

    def test_evaluate_skip_condition_returns_false_when_no_skip_condition(self):
        # Given
        skip_conditions = None

        # When
        condition = evaluate_skip_conditions(skip_conditions, get_schema_mock(), {}, AnswerStore({}))

        # Then
        self.assertFalse(condition)

    def test_evaluate_not_set_when_rules_should_return_true(self):
        when = {
            'when': [
                {
                    'id': 'my_answers',
                    'condition': 'not set'
                }
            ]
        }
        answer_store = AnswerStore({})

        self.assertTrue(evaluate_when_rules(when['when'], get_schema_mock(), {}, answer_store, None))

    def test_go_to_next_question_for_multiple_answers(self):
        # Given
        goto = {
            'id': 'next-question',
            'when': [
                {
                    'id': 'my_answer',
                    'condition': 'equals',
                    'value': 'Yes'
                },
                {
                    'id': 'my_other_answer',
                    'condition': 'equals',
                    'value': '2'
                }
            ]
        }
        answer_store = AnswerStore({})
        answer_store.add_or_update(Answer(answer_id='my_answer', value='Yes'))
        answer_store.add_or_update(Answer(answer_id='my_other_answer', value='2'))

        self.assertTrue(evaluate_goto(goto, get_schema_mock(), {}, answer_store))

    def test_do_not_go_to_next_question_for_multiple_answers(self):
        # Given
        goto_rule = {
            'id': 'next-question',
            'when': [
                {
                    'id': 'my_answer',
                    'condition': 'equals',
                    'value': 'Yes'
                },
                {
                    'id': 'my_other_answer',
                    'condition': 'equals',
                    'value': '2'
                }
            ]
        }
        answer_store = AnswerStore({})
        answer_store.add_or_update(Answer(answer_id='my_answer', value='No'))

        self.assertFalse(evaluate_goto(goto_rule, get_schema_mock(), {}, answer_store))

    def test_should_go_to_next_question_when_condition_is_meta_and_answer_type(self):
        # Given
        goto_rule = {
            'id': 'next-question',
            'when': [
                {
                    'id': 'my_answer',
                    'condition': 'equals',
                    'value': 'Yes'
                },
                {
                    'condition': 'equals',
                    'meta': 'sexual_identity',
                    'value': True
                }
            ]
        }
        answer_store = AnswerStore({})
        answer_store.add_or_update(Answer(answer_id='my_answer', value='Yes'))
        metadata = {'sexual_identity': True}

        # When
        goto = evaluate_goto(goto_rule, get_schema_mock(), metadata, answer_store)

        # Then
        self.assertTrue(goto)

    def test_meta_comparison_missing(self):
        # Given
        goto_rule = {
            'id': 'next-question',
            'when': [
                {
                    'condition': 'equals',
                    'meta': 'variant_flags.does_not_exist.does_not_exist',
                    'value': True
                }
            ]
        }
        answer_store = AnswerStore({})
        answer_store.add_or_update(Answer(answer_id='my_answer', value='Yes'))
        metadata = {'varient_flags': {'sexual_identity': True}}

        # When
        goto = evaluate_goto(goto_rule, get_schema_mock(), metadata, answer_store)

        # Then
        self.assertFalse(goto)

    def test_should_not_go_to_next_question_when_second_condition_fails(self):
        # Given
        goto_rule = {
            'id': 'next-question',
            'when': [
                {
                    'id': 'my_answer',
                    'condition': 'equals',
                    'value': 'Yes'
                },
                {
                    'condition': 'equals',
                    'meta': 'sexual_identity',
                    'value': False
                }
            ]
        }
        answer_store = AnswerStore({})
        answer_store.add_or_update(Answer(answer_id='my_answer', value='Yes'))
        metadata = {'sexual_identity': True}

        # When
        goto = evaluate_goto(goto_rule, get_schema_mock(), metadata, answer_store)

        # Then
        self.assertFalse(goto)

    def test_when_rule_comparing_answer_values(self):
        answers = {
            'low': Answer(answer_id='low', value=1),
            'medium': Answer(answer_id='medium', value=5),
            'high': Answer(answer_id='high', value=10),
            'list_answer': Answer(answer_id='list_answer', value=['a', 'abc', 'cba']),
            'other_list_answer': Answer(answer_id='other_list_answer', value=['x', 'y', 'z']),
            'other_list_answer_2': Answer(answer_id='other_list_answer_2', value=['a', 'abc', 'cba']),
            'text_answer': Answer(answer_id='small_string', value='abc'),
            'other_text_answer': Answer(answer_id='other_string', value='xyz'),
        }

        # An answer that won't be added to the answer store.
        missing_answer = Answer(answer_id='missing', value=1)

        param_list = [
            (answers['medium'], 'equals', answers['medium'], True),
            (answers['medium'], 'equals', answers['low'], False),
            (answers['medium'], 'greater than', answers['low'], True),
            (answers['medium'], 'greater than', answers['high'], False),
            (answers['medium'], 'less than', answers['high'], True),
            (answers['medium'], 'less than', answers['low'], False),
            (answers['medium'], 'equals', missing_answer, False),
            (answers['list_answer'], 'contains', answers['text_answer'], True),
            (answers['list_answer'], 'contains', answers['other_text_answer'], False),
            (answers['list_answer'], 'not contains', answers['other_text_answer'], True),
            (answers['list_answer'], 'not contains', answers['text_answer'], False),
            (answers['list_answer'], 'contains any', answers['other_list_answer_2'], True),
            (answers['list_answer'], 'contains any', answers['other_list_answer'], False),
            (answers['list_answer'], 'contains all', answers['other_list_answer'], False),
            (answers['list_answer'], 'contains all', answers['other_list_answer_2'], True),
            (answers['text_answer'], 'equals any', answers['list_answer'], True),
            (answers['text_answer'], 'equals any', answers['other_list_answer'], False),
            (answers['text_answer'], 'not equals any', answers['other_list_answer'], True),
            (answers['text_answer'], 'not equals any', answers['list_answer'], False)
        ]

        for lhs, comparison, rhs, expected_result in param_list:
            # Given
            with self.subTest(lhs=lhs, comparison=comparison, rhs=rhs, expected_result=expected_result):
                answer_store = AnswerStore({})
                for answer in answers.values():
                    answer_store.add_or_update(answer)

                when = [{
                    'id': lhs.answer_id,
                    'condition': comparison,
                    'comparison_id': rhs.answer_id
                }]

                self.assertEqual(evaluate_when_rules(when, get_schema_mock(), {}, answer_store, None), expected_result)

    def test_evaluate_when_rule_raises_if_bad_when_condition(self):
        when = {
            'when': [
                {
                    'condition': 'not set'
                }
            ]
        }
        answer_store = AnswerStore({})
        with self.assertRaises(Exception):
            evaluate_when_rules(when['when'], get_schema_mock(), {}, answer_store, None)

    def test_routing_ignores_answers_not_on_path(self):
        when = {
            'when': [
                {
                    'id': 'some-answer',
                    'condition': 'equals',
                    'value': 'some value'
                }
            ]
        }
        answer_store = AnswerStore({})
        answer_store.add_or_update(Answer(
            answer_id='some-answer',
            value='some value',
        ))

        routing_path = [
            Location('test_block_id')
        ]
        self.assertTrue(evaluate_when_rules(when['when'], get_schema_mock(), {}, answer_store, None))

        with patch('app.questionnaire.rules._is_answer_on_path', return_value=False):
            self.assertFalse(
                evaluate_when_rules(when['when'], get_schema_mock(), {}, answer_store, routing_path=routing_path))

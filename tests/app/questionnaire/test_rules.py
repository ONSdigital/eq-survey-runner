from unittest import TestCase
from datetime import datetime

from app.data_model.answer_store import AnswerStore, Answer
from app.questionnaire.location import Location
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.rules import evaluate_rule, evaluate_date_rule, evaluate_goto, evaluate_repeat, \
    evaluate_skip_conditions, evaluate_when_rules, get_answer_ids_on_routing_path


class TestRules(TestCase):  # pylint: disable=too-many-public-methods
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
        answer_store.add(Answer(answer_id='my_answer', value='Yes'))

        self.assertTrue(evaluate_goto(goto, {}, answer_store, 0))

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
        answer_store.add(Answer(answer_id='my_answer', value='No'))

        self.assertFalse(evaluate_goto(goto_rule, {}, answer_store, 0))

    def test_evaluate_goto_returns_true_when_value_contained_in_list(self):

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
        answer_store.add(Answer(answer_id='my_answers', value=['answer1', 'answer2', 'answer3']))

        self.assertTrue(evaluate_goto(goto, {}, answer_store, 0))

    def test_evaluate_goto_returns_true_when_value_not_contained_in_list(self):

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
        answer_store.add(Answer(answer_id='my_answers', value=['answer2', 'answer3']))

        self.assertTrue(evaluate_goto(goto, {}, answer_store, 0))

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
        answer_store.add(Answer(answer_id='this', value='value'))

        # When
        condition = evaluate_skip_conditions(skip_conditions, {}, answer_store)

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
        answer_store.add(Answer(answer_id='that', value='other value'))

        self.assertTrue(evaluate_skip_conditions(skip_conditions, {}, answer_store))

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
        answer_store.add(Answer(answer_id='this', value='value'))
        answer_store.add(Answer(answer_id='that', value='other value'))

        # When
        condition = evaluate_skip_conditions(skip_conditions, {}, answer_store)

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
        answer_store.add(Answer(answer_id='this', value='not correct'))
        answer_store.add(Answer(answer_id='that', value='not correct'))

        # When
        condition = evaluate_skip_conditions(skip_conditions, {}, answer_store)

        # Then
        self.assertFalse(condition)

    def test_evaluate_skip_condition_returns_false_when_no_skip_condition(self):
        # Given
        skip_conditions = None

        # When
        condition = evaluate_skip_conditions(skip_conditions, {}, AnswerStore({}))

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

        self.assertTrue(evaluate_when_rules(when, {}, answer_store, 0))

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
        answer_store.add(Answer(answer_id='my_answer', value='Yes'))
        answer_store.add(Answer(answer_id='my_other_answer', value='2'))

        self.assertTrue(evaluate_goto(goto, {}, answer_store, 0))

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
        answer_store.add(Answer(answer_id='my_answer', value='No'))

        self.assertFalse(evaluate_goto(goto_rule, {}, answer_store, 0))

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
        answer_store.add(Answer(answer_id='my_answer', value='Yes'))
        metadata = {'sexual_identity': True}

        # When
        goto = evaluate_goto(goto_rule, metadata, answer_store, 0)

        # Then
        self.assertTrue(goto)

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
        answer_store.add(Answer(answer_id='my_answer', value='Yes'))
        metadata = {'sexual_identity': True}

        # When
        goto = evaluate_goto(goto_rule, metadata, answer_store, 0)

        # Then
        self.assertFalse(goto)

    def test_should_repeat_for_answer_answer_value(self):
        questionnaire = {
            'survey_id': '021',
            'data_version': '0.0.1',
            'sections': [{
                'id': 'section1',
                'groups': [
                    {
                        'id': 'group-1',
                        'blocks': [
                            {
                                'id': 'block-1',
                                'questions': [{
                                    'id': 'question-2',
                                    'answers': [
                                        {
                                            'id': 'my_answer',
                                            'type': 'TextField'
                                        }
                                    ]
                                }]
                            }
                        ]
                    }
                ]
            }]
        }

        schema = QuestionnaireSchema(questionnaire)

        # Given
        repeat = {
            'answer_id': 'my_answer',
            'type': 'answer_value'
        }
        answer_store = AnswerStore({})
        answer_store.add(Answer(answer_id='my_answer', value='3'))

        current_path = [Location('group-1', 0, 'block-1')]

        # When
        answer_on_path = get_answer_ids_on_routing_path(schema, current_path)
        number_of_repeats = evaluate_repeat(repeat, answer_store, answer_on_path)

        self.assertEqual(number_of_repeats, 3)

    def test_should_repeat_for_answer_answer_count(self):
        questionnaire = {
            'survey_id': '021',
            'data_version': '0.0.1',
            'sections': [{
                'id': 'section1',
                'groups': [
                    {
                        'id': 'group-1',
                        'blocks': [
                            {
                                'id': 'block-1',
                                'questions': [{
                                    'id': 'question-2',
                                    'answers': [
                                        {
                                            'id': 'my_answer',
                                            'type': 'TextField'
                                        }
                                    ]
                                }]
                            }
                        ]
                    }
                ]
            }]
        }

        schema = QuestionnaireSchema(questionnaire)

        # Given
        repeat = {
            'answer_id': 'my_answer',
            'type': 'answer_count'
        }
        answer_store = AnswerStore({})
        answer_store.add(Answer(answer_id='my_answer', value='3'))
        answer_store.add(Answer(answer_id='my_answer', value='4', answer_instance=1))

        current_path = [Location('group-1', 0, 'block-1')]

        # When
        answer_on_path = get_answer_ids_on_routing_path(schema, current_path)
        number_of_repeats = evaluate_repeat(repeat, answer_store, answer_on_path)

        self.assertEqual(number_of_repeats, 2)

    def test_should_repeat_for_answer_answer_count_minus_one(self):
        questionnaire = {
            'survey_id': '021',
            'data_version': '0.0.1',
            'sections': [{
                'id': 'section1',
                'groups': [
                    {
                        'id': 'group-1',
                        'blocks': [
                            {
                                'id': 'block-1',
                                'questions': [{
                                    'id': 'question-2',
                                    'answers': [
                                        {
                                            'id': 'my_answer',
                                            'type': 'TextField'
                                        }
                                    ]
                                }]
                            }
                        ]
                    }
                ]
            }]
        }

        schema = QuestionnaireSchema(questionnaire)

        # Given
        repeat = {
            'answer_id': 'my_answer',
            'type': 'answer_count_minus_one'
        }
        answer_store = AnswerStore({})
        answer_store.add(Answer(answer_id='my_answer', value='3'))
        answer_store.add(Answer(answer_id='my_answer', value='4', answer_instance=1))

        current_path = [Location('group-1', 0, 'block-1')]

        # When
        answer_on_path = get_answer_ids_on_routing_path(schema, current_path)
        number_of_repeats = evaluate_repeat(repeat, answer_store, answer_on_path)

        self.assertEqual(number_of_repeats, 1)

    def test_should_minus_one_from_maximum_repeats(self):
        questionnaire = {
            'survey_id': '021',
            'data_version': '0.0.1',
            'sections': [{
                'id': 'section1',
                'groups': [
                    {
                        'id': 'group-1',
                        'blocks': [
                            {
                                'id': 'block-1',
                                'questions': [{
                                    'id': 'question-2',
                                    'answers': [
                                        {
                                            'id': 'my_answer',
                                            'type': 'TextField'
                                        }
                                    ]
                                }]
                            }
                        ]
                    }
                ]
            }]
        }

        schema = QuestionnaireSchema(questionnaire)

        # Given
        repeat = {
            'answer_id': 'my_answer',
            'type': 'answer_count_minus_one'
        }
        answer_store = AnswerStore({})
        for i in range(27):
            answer_store.add(Answer(answer_id='my_answer', value='3', answer_instance=i))

        current_path = [Location('group-1', 0, 'block-1')]

        # When
        answer_on_path = get_answer_ids_on_routing_path(schema, current_path)
        number_of_repeats = evaluate_repeat(repeat, answer_store, answer_on_path)

        self.assertEqual(number_of_repeats, 24)

    def test_evaluate_when_rules_condition_is_not_met(self):
        # Given
        answer_1 = Answer(
            answer_id='my_answers',
            answer_instance=0,
            group_instance=0,
            value=10,
        )
        answer_2 = Answer(
            answer_id='my_answers',
            answer_instance=1,
            group_instance=0,
            value=20,
        )
        answer_store = AnswerStore({})
        answer_store.add(answer_1)
        answer_store.add(answer_2)

        when = {
            'id': 'next-question',
            'when': [
                {
                    'id': 'my_answers',
                    'condition': 'not set',
                    'value': '2'
                }
            ]
        }

        # When
        with self.assertRaises(Exception) as err:
            evaluate_when_rules(when['when'], None, answer_store, 0)
        self.assertEqual('Multiple answers (2) found evaluating when rule for answer (my_answers)', str(err.exception))

class TestDateRules(TestCase):

    def test_evaluate_date_rule_equals_with_value_now(self):

        when = {
            'id': 'date-answer',
            'condition': 'equals',
            'date_comparison': {
                'value': 'now'
            }
        }

        answer_value = datetime.utcnow().strftime('%Y-%m-%d')
        result = evaluate_date_rule(when, None, 0, None, answer_value)
        self.assertTrue(result)

        answer_value = '2000-01-01'
        result = evaluate_date_rule(when, None, 0, None, answer_value)
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
        result = evaluate_date_rule(when, None, 0, None, answer_value)
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
        result = evaluate_date_rule(when, None, 0, None, answer_value)
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
        result = evaluate_date_rule(when, None, 0, None, answer_value)
        self.assertTrue(result)

        answer_value = '2018-01'
        result = evaluate_date_rule(when, None, 0, None, answer_value)
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
        result = evaluate_date_rule(when, None, 0, metadata, answer_value)
        self.assertTrue(result)

        answer_value = '2016-06-12'
        result = evaluate_date_rule(when, None, 0, metadata, answer_value)
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
        answer_store.add(Answer(answer_id='compare_date_answer', value='2018-02-03'))

        answer_value = '2018-02-04'
        result = evaluate_date_rule(when, answer_store, 0, None, answer_value)
        self.assertTrue(result)

        answer_value = '2018-02-03'
        result = evaluate_date_rule(when, answer_store, 0, None, answer_value)
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
        answer_store.add(Answer(answer_id='date_answer', value='2018-02-01'))

        self.assertFalse(evaluate_goto(goto_rule, {}, answer_store, 0))

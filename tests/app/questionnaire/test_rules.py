from unittest import TestCase

from app.data_model.answer_store import AnswerStore, Answer
from app.questionnaire.rules import evaluate_rule, evaluate_goto, evaluate_repeat, evaluate_skip_condition, \
    evaluate_when_rules


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
        answer_store = AnswerStore()
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
        answer_store = AnswerStore()
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
        answer_store = AnswerStore()
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
        answer_store = AnswerStore()
        answer_store.add(Answer(answer_id='my_answers', value=['answer2', 'answer3']))

        self.assertTrue(evaluate_goto(goto, {}, answer_store, 0))

    def test_evaluate_skip_condition_returns_true_when_this_rule_true(self):
        # Given
        skip_condition = [
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
        answer_store = AnswerStore()
        answer_store.add(Answer(answer_id='this', value='value'))

        # When
        condition = evaluate_skip_condition(skip_condition, {}, answer_store)

        # Given
        self.assertTrue(condition)

    def test_evaluate_skip_condition_returns_true_when_that_rule_true(self):

        skip_condition = [
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
        answer_store = AnswerStore()
        answer_store.add(Answer(answer_id='that', value='other value'))

        self.assertTrue(evaluate_skip_condition(skip_condition, {}, answer_store))

    def test_evaluate_skip_condition_returns_true_when_more_than_one_rule_is_true(self):
        # Given
        skip_condition = [
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
        answer_store = AnswerStore()
        answer_store.add(Answer(answer_id='this', value='value'))
        answer_store.add(Answer(answer_id='that', value='other value'))

        # When
        condition = evaluate_skip_condition(skip_condition, {}, answer_store)

        # Then
        self.assertTrue(condition)

    def test_evaluate_skip_condition_returns_false_when_both_or_rules_false(self):
        # Given
        skip_condition = [
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
        answer_store = AnswerStore()
        answer_store.add(Answer(answer_id='this', value='not correct'))
        answer_store.add(Answer(answer_id='that', value='not correct'))

        # When
        condition = evaluate_skip_condition(skip_condition, {}, answer_store)

        # Then
        self.assertFalse(condition)

    def test_evaluate_skip_condition_returns_false_when_no_skip_condition(self):
        # Given
        skip_condition = None

        # When
        condition = evaluate_skip_condition(skip_condition, {}, AnswerStore())

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
        answer_store = AnswerStore()

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
        answer_store = AnswerStore()
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
        answer_store = AnswerStore()
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
        answer_store = AnswerStore()
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
        answer_store = AnswerStore()
        answer_store.add(Answer(answer_id='my_answer', value='Yes'))
        metadata = {'sexual_identity': True}

        # When
        goto = evaluate_goto(goto_rule, metadata, answer_store, 0)

        # Then
        self.assertFalse(goto)

    def test_should_repeat_for_answer_answer_value(self):
        # Given
        repeat = {
            'answer_id': 'my_answer',
            'type': 'answer_value'
        }
        answer_store = AnswerStore()
        answer_store.add(Answer(answer_id='my_answer', value='3'))

        # When
        number_of_repeats = evaluate_repeat(repeat, answer_store)

        self.assertEqual(number_of_repeats, 3)

    def test_should_repeat_for_answer_answer_count(self):
        # Given
        repeat = {
            'answer_id': 'my_answer',
            'type': 'answer_count'
        }
        answer_store = AnswerStore()
        answer_store.add(Answer(answer_id='my_answer', value='3'))
        answer_store.add(Answer(answer_id='my_answer', value='4', answer_instance=1))

        # When
        number_of_repeats = evaluate_repeat(repeat, answer_store)

        self.assertEqual(number_of_repeats, 2)

    def test_should_repeat_for_answer_answer_count_minus_one(self):
        # Given
        repeat = {
            'answer_id': 'my_answer',
            'type': 'answer_count_minus_one'
        }
        answer_store = AnswerStore()
        answer_store.add(Answer(answer_id='my_answer', value='3'))
        answer_store.add(Answer(answer_id='my_answer', value='4', answer_instance=1))

        # When
        number_of_repeats = evaluate_repeat(repeat, answer_store)

        self.assertEqual(number_of_repeats, 1)

    def test_should_minus_one_from_maximum_repeats(self):
        # Given
        repeat = {
            'answer_id': 'my_answer',
            'type': 'answer_count_minus_one'
        }
        answer_store = AnswerStore()
        for i in range(27):
            answer_store.add(Answer(answer_id='my_answer', value='3', answer_instance=i))

        # When
        number_of_repeats = evaluate_repeat(repeat, answer_store)

        self.assertEqual(number_of_repeats, 24)

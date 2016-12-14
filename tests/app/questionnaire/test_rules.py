from unittest import TestCase

from app.data_model.answer_store import AnswerStore, Answer
from app.questionnaire.rules import evaluate_rule, evaluate_goto, evaluate_repeat


class TestRules(TestCase):
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

    def test_should_repeat_for_answer_answer_value(self):
        # Given
        repeat = {
            'answer_id': 'my_answer',
            'type': 'answer_value'
        }
        answer_store = AnswerStore()
        answer_store.add(Answer(answer_id='my_answer', value='3'))

        # When
        number_of_repeats = evaluate_repeat(repeat,answer_store)

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

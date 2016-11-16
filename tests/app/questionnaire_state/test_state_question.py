import unittest

from mock import MagicMock
from app.questionnaire_state.state_question import StateQuestion


class TestStateQuestion(unittest.TestCase):

    def test_remove_answer_single_answer(self):
        answer = MagicMock()
        question = StateQuestion('question_id', MagicMock())

        question.answers.append(answer)

        self.assertTrue(answer in question.answers)
        self.assertTrue(answer in question.children)
        self.assertEqual(len(question.answers), 1)
        self.assertEqual(len(question.children), 1)

        question.remove_answer(answer)

        self.assertFalse(answer in question.answers)
        self.assertFalse(answer in question.children)
        self.assertEqual(len(question.answers), 0)
        self.assertEqual(len(question.children), 0)

    def test_remove_answer_multiple_answers(self):
        answer1 = MagicMock()
        answer2 = MagicMock()

        question = StateQuestion('question_id', MagicMock())
        question.answers.append(answer1)
        question.answers.append(answer2)

        self.assertEqual(len(question.answers), 2)
        self.assertTrue(answer1 in question.answers)
        self.assertTrue(answer2 in question.answers)

        question.remove_answer(answer1)

        self.assertEqual(len(question.answers), 1)
        self.assertFalse(answer1 in question.answers)
        self.assertTrue(answer2 in question.answers)

    def test_update_state_initialise_non_repeating(self):

        question = StateQuestion('question_id', MagicMock())

        answer1 = MagicMock()
        question.answers.append(answer1)

        question.update_state({})
        self.assertEqual(len(question.children), 1)

    def test_update_state_initialise_repeating(self):

        question = StateQuestion('question_id', MagicMock())
        question.schema_item.type = 'RepeatingAnswer'

        answer1 = MagicMock()
        answer1.schema_item.id = 'answer_id'
        question.answers.append(answer1)

        question.update_state({
            'answer_id': 'answer_value',
            'answer_id_1': 'answer_value_1'
        })
        self.assertEqual(len(question.children), 2)

    def test_update_state_single_answer(self):

        question = StateQuestion('question_id', MagicMock())
        question.schema_item.type = 'RepeatingAnswer'

        answer1 = MagicMock()
        answer1.schema_item.id = 'answer_id'
        question.answers.append(answer1)
        question.update_state({
            'answer_id': 'answer_value',
        })
        self.assertEqual(len(question.children), 1)

    def test_update_state_multiple_answers_in_schema(self):

        question = StateQuestion('question_id', MagicMock())
        question.schema_item.type = 'RepeatingAnswer'

        answer1 = MagicMock()
        answer1.schema_item.id = 'answer_one'

        answer2 = MagicMock()
        answer2.schema_item.id = 'answer_two'

        answer3 = MagicMock()
        answer3.schema_item.id = 'answer_three'

        question.answers.append(answer1)
        question.answers.append(answer2)

        question.update_state({
            'answer_one': 'answer_one_value',
            'answer_one_1': 'answer_one_value_1',
            'answer_two': 'answer_two_value',
        })

        self.assertEqual(len(question.children), 3)

        question.answers.clear()

        question.answers.append(answer1)
        question.answers.append(answer2)
        question.answers.append(answer3)

        question.update_state({
            'answer_one': 'answer_one_value',
            'answer_one_1': 'answer_one_value_1',
            'answer_two': 'answer_two_value',
            'answer_two_1': 'answer_two_value_1',
            'answer_two_2': 'answer_two_value_2',
            'answer_three': 'answer_three_value',
        })

        self.assertEqual(len(question.children), 6)

    def test_update_state_non_repeating_multiple_answers(self):
        question = StateQuestion('question_id', MagicMock())

        answer1 = MagicMock()
        answer1.schema_item.id = 'answer_one'

        answer2 = MagicMock()
        answer2.schema_item.id = 'answer_two'

        answer3 = MagicMock()
        answer3.schema_item.id = 'answer_three'

        question.answers.append(answer1)
        question.answers.append(answer2)
        question.answers.append(answer3)

        question.update_state({
            'answer_one': 'answer_one_value',
            'answer_two': 'answer_two_value',
            'answer_three': 'answer_three_value',
        })

        self.assertEqual(len(question.children), 3)

    def test_get_instance_id_when_no_existing_answers_should_return_zero(self):
        question = StateQuestion('question_id', MagicMock())
        new_instance_id = question._get_instance_id([], 'answer', 0)
        self.assertEqual(new_instance_id, 0)

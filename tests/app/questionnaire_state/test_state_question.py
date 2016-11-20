import unittest

from mock import MagicMock

from app.questionnaire_state.state_answer import StateAnswer
from app.questionnaire_state.state_question import StateQuestion
from app.schema.answer import Answer


def side_effect_create_answer_state(answer_instance, parent):
    new_answer = MagicMock()
    new_answer.answer_instance = answer_instance
    parent.answers.append(new_answer)
    return new_answer


class TestStateQuestion(unittest.TestCase):

    def test_add_answers_to_question(self):
        # Given
        answer = MagicMock()
        question = StateQuestion('question_id', MagicMock())

        # When
        question.answers.append(answer)

        # Then
        self.assertTrue(answer in question.answers)
        self.assertTrue(answer in question.children)
        self.assertEqual(len(question.answers), 1)
        self.assertEqual(len(question.children), 1)

    def test_add_multiple_answers_to_question(self):
        # Given
        answer1 = MagicMock()
        answer2 = MagicMock()
        question = StateQuestion('question_id', MagicMock())

        # When
        question.answers.append(answer1)
        question.answers.append(answer2)

        # Then
        self.assertEqual(len(question.answers), 2)
        self.assertEqual(len(question.children), 2)
        self.assertTrue(answer1 in question.answers)
        self.assertTrue(answer1 in question.children)
        self.assertTrue(answer2 in question.answers)
        self.assertTrue(answer2 in question.children)

    def test_remove_answer_single_answer(self):
        # Given
        answer = MagicMock()
        question = StateQuestion('question_id', MagicMock())
        question.answers.append(answer)

        # When
        question.remove_answer(answer)

        # Then
        self.assertFalse(answer in question.answers)
        self.assertFalse(answer in question.children)
        self.assertEqual(len(question.answers), 0)
        self.assertEqual(len(question.children), 0)

    def test_remove_answer_multiple_answers(self):
        # Given
        answer1 = MagicMock()
        answer2 = MagicMock()

        question = StateQuestion('question_id', MagicMock())
        question.answers.append(answer1)
        question.answers.append(answer2)

        # When
        question.remove_answer(answer1)

        # Then
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

        question_state = StateQuestion('question_id', MagicMock())
        question_state.schema_item.type = 'RepeatingAnswer'
        question_state.schema_item.answers = [Answer('answer_id')]
        question_state.schema_item.answers[0].widget = MagicMock()

        answer_state = MagicMock()
        answer_state.id = 'answer_id'
        answer_state.answer_instance = 0

        question_state.answers.append(answer_state)
        question_state.update_state({
            'answer_id': 'answer_value',
            'answer_id_1': 'answer_value_1'
        })
        self.assertEqual(len(question_state.answers), 2)

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

        answer1 = Answer('answer_one')
        answer2 = Answer('answer_two')

        answer1.widget = MagicMock()
        answer2.widget = MagicMock()

        question.schema_item.answers = [answer1, answer2]

        question.update_state({
            'answer_one': 'answer_one_value',
            'answer_one_1': 'answer_one_value_1',
            'answer_two': 'answer_two_value',
        })

        self.assertEqual(len(question.children), 3)

        question.update_state({
            'answer_one': 'answer_one_value',
            'answer_two': 'answer_two_value',
            'answer_two_3': 'answer_two_value_3',
            'answer_two_2': 'answer_two_value_2',
        })

        self.assertEqual(len(question.children), 5)

    def test_update_state_multiple_repeating_answers(self):

        question_state = StateQuestion('question_id', MagicMock())
        question_state.schema_item.type = 'RepeatingAnswer'

        answers = []
        for x in range(3):
            answer = Answer('answer'+str(x))
            answer.widget = MagicMock()
            answers.append(answer)
        question_state.schema_item.answers = answers

        answer1 = StateAnswer('answer0', MagicMock())
        answer2 = StateAnswer('answer1', MagicMock())
        answer3 = StateAnswer('answer2', MagicMock())

        question_state.answers = [answer1, answer2, answer3]

        question_state.update_state({
            'answer0': 'answer_one_value',
            'answer0_1': 'answer_one_value_1',
            'answer1': 'answer_two_value',
            'answer1_1': 'answer_two_value_1',
            'answer1_2': 'answer_two_value_2',
            'answer2': 'answer_three_value',
        })

        self.assertEqual(len(question_state.answers), 6)

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

    def test_extract_answer_instance_id(self):
        answer_id, answer_index = StateQuestion._extract_answer_instance_id('')
        self.assertEqual(answer_id, '')
        self.assertEqual(answer_index, 0)

        answer_id, answer_index = StateQuestion._extract_answer_instance_id('abcdefg')
        self.assertEqual(answer_id, 'abcdefg')
        self.assertEqual(answer_index, 0)

        answer_id, answer_index = StateQuestion._extract_answer_instance_id('abcdefg_')
        self.assertEqual(answer_id, 'abcdefg_')
        self.assertEqual(answer_index, 0)

        answer_id, answer_index = StateQuestion._extract_answer_instance_id('abcdefg_0')
        self.assertEqual(answer_id, 'abcdefg')
        self.assertEqual(answer_index, 0)

        answer_id, answer_index = StateQuestion._extract_answer_instance_id('abcdefg_1')
        self.assertEqual(answer_id, 'abcdefg')
        self.assertEqual(answer_index, 1)

        answer_id, answer_index = StateQuestion._extract_answer_instance_id('abcdefg_1_2')
        self.assertEqual(answer_id, 'abcdefg_1')
        self.assertEqual(answer_index, 2)

        answer_id, answer_index = StateQuestion._extract_answer_instance_id('_1')
        self.assertEqual(answer_id, '_1')
        self.assertEqual(answer_index, 0)

        answer_id, answer_index = StateQuestion._extract_answer_instance_id('1234_1')
        self.assertEqual(answer_id, '1234')
        self.assertEqual(answer_index, 1)

        answer_id, answer_index = StateQuestion._extract_answer_instance_id('abcdefg_12345')
        self.assertEqual(answer_id, 'abcdefg')
        self.assertEqual(answer_index, 12345)

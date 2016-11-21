import unittest

from mock import MagicMock

from app.questionnaire_state.state_question import StateQuestion


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

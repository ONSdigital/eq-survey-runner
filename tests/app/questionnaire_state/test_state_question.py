import unittest

from mock import MagicMock
from app.questionnaire_state.state_question import StateQuestion


class TestStateQuestion(unittest.TestCase):

    def test_remove_answer_single_answer(self):
        answer = MagicMock()
        question = StateQuestion('question_id', MagicMock)

        question.answers.append(answer)

        self.assertTrue(answer in question.answers)
        self.assertEqual(len(question.answers), 1)

        question.remove_answer(answer)

        self.assertFalse(answer in question.answers)
        self.assertEqual(len(question.answers), 0)

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

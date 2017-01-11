import unittest

from app.schema.answer import Answer
from app.schema.question import Question


class QuestionModelTest(unittest.TestCase):
    def test_basics(self):
        question = Question()

        question.id = 'some-id'
        question.title = 'my question object'
        question.description = 'fill this in'

        answer1 = Answer()
        answer1.id = 'answer-1'
        answer2 = Answer()
        answer2.id = 'answer-2'

        question.add_answer(answer1)
        question.add_answer(answer2)

        self.assertEqual(question.id, 'some-id')
        self.assertEqual(question.title, 'my question object')
        self.assertEqual(question.description, 'fill this in')
        self.assertIsNone(question.container)
        self.assertEqual(len(question.answers), 2)
        self.assertEqual(question.answers[0], answer1)
        self.assertEqual(question.answers[1], answer2)

        self.assertEqual(answer1.container, question)
        self.assertEqual(answer2.container, question)

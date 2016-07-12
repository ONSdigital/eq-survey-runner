from app.schema.question import Question
from app.schema.answer import Answer
import unittest


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

        self.assertEquals(question.id, 'some-id')
        self.assertEquals(question.title, 'my question object')
        self.assertEquals(question.description, 'fill this in')
        self.assertIsNone(question.container)
        self.assertEquals(len(question.answers), 2)
        self.assertEquals(question.answers[0], answer1)
        self.assertEquals(question.answers[1], answer2)

        self.assertEquals(answer1.container, question)
        self.assertEquals(answer2.container, question)

from app.schema.answer import Answer
import unittest


class AnswerModelTest(unittest.TestCase):
    def test_basics(self):
        answer = Answer()

        answer.id = 'some-id'
        answer.label = 'my answer object'
        answer.guidance = 'fill this in'
        answer.type = 'some-type'
        answer.code = 'code'
        answer.container = None

        self.assertEquals(answer.id, 'some-id')
        self.assertEquals(answer.label, 'my answer object')
        self.assertEquals(answer.guidance, 'fill this in')
        self.assertEquals(answer.type, 'some-type')
        self.assertEquals(answer.code, 'code')
        self.assertIsNone(answer.container)

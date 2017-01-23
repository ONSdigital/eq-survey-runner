import unittest

from app.schema.answer import Answer


class AnswerModelTest(unittest.TestCase):
    def test_basics(self):
        answer = Answer()

        answer.id = 'some-id'
        answer.label = 'my answer object'
        answer.guidance = 'fill this in'
        answer.type = 'some-type'
        answer.code = 'code'
        answer.container = None

        self.assertEqual(answer.id, 'some-id')
        self.assertEqual(answer.label, 'my answer object')
        self.assertEqual(answer.guidance, 'fill this in')
        self.assertEqual(answer.type, 'some-type')
        self.assertEqual(answer.code, 'code')
        self.assertIsNone(answer.container)

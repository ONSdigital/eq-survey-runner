from app.model.question import Question
from app.model.response import Response
import unittest
import json


class QuestionModelTest(unittest.TestCase):
    def test_basics(self):
        question = Question()

        question.id = 'some-id'
        question.title = 'my question object'
        question.description = 'fill this in'

        response1 = Response()
        response2 = Response()

        question.add_response(response1)
        question.add_response(response2)

        self.assertEquals(question.id, 'some-id')
        self.assertEquals(question.title, 'my question object')
        self.assertEquals(question.description, 'fill this in')
        self.assertIsNone(question.container)
        self.assertEquals(len(question.responses), 2)
        self.assertEquals(question.responses[0], response1)
        self.assertEquals(question.responses[1], response2)

        self.assertEquals(response1.container, question)
        self.assertEquals(response2.container, question)

    def test_to_json(self):
        question = Question()

        question.id = 'some-id'
        question.title = 'my question object'
        question.description = 'fill this in'

        response1 = Response()
        response2 = Response()

        question.add_response(response1)
        question.add_response(response2)

        json_str = json.dumps(question.to_json())
        json_obj = json.loads(json_str)

        self.assertEquals(json_obj['id'], 'some-id')
        self.assertEquals(json_obj['title'], 'my question object')
        self.assertEquals(json_obj['description'], 'fill this in')
        self.assertEquals(len(json_obj['responses']), 2)

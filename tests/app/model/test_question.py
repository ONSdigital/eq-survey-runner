from app.model.question import Question
from app.model.response import Response
import unittest


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

    def test_get_item_by_id(self):
        question = Question()

        question.id = 'some-id'
        question.title = 'my question object'
        question.description = 'fill this in'

        response1 = Response()

        response1.id = 'response-1'
        response1.label = 'my response object'
        response1.guidance = 'fill this in'
        response1.type = 'some-type'
        response1.code = 'code1'

        response2 = Response()

        response2.id = 'response-2'
        response2.label = 'another response object'
        response2.guidance = 'fill this in'
        response2.type = 'another-type'
        response2.code = 'code2'

        question.add_response(response1)
        question.add_response(response2)

        self.assertEquals(question.get_item_by_id('some-id'), question)
        self.assertIsNone(question.get_item_by_id('another-id'))
        self.assertEquals(question.get_item_by_id('response-1'), response1)
        self.assertEquals(question.get_item_by_id('response-2'), response2)

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
        response1.id = 'response-1'
        response2 = Response()
        response2.id = 'response-2'

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
        response1.id = 'response-1'
        response2 = Response()
        response2.id = 'response-2'

        question.add_response(response1)
        question.add_response(response2)

        json_str = json.dumps(question.to_json())
        json_obj = json.loads(json_str)

        self.assertEquals(json_obj['id'], 'some-id')
        self.assertEquals(json_obj['title'], 'my question object')
        self.assertEquals(json_obj['description'], 'fill this in')
        self.assertEquals(len(json_obj['responses']), 2)

    def test_equivalence(self):
        question1 = Question()

        question1.id = 'some-id'
        question1.title = 'my question object'
        question1.description = 'fill this in'

        response1_1 = Response()
        response1_1.id = 'response-1'
        response1_2 = Response()
        response1_2.id = 'response-2'

        question1.add_response(response1_1)
        question1.add_response(response1_2)

        question2 = Question()

        question2.id = 'some-id'
        question2.title = 'my question object'
        question2.description = 'fill this in'

        response2_1 = Response()
        response2_1.id = 'response-1'
        response2_2 = Response()
        response2_2.id = 'response-2'

        question2.add_response(response2_1)
        question2.add_response(response2_2)

        self.assertEquals(question1, question2)
        self.assertEquals(question2, question1)

        question1.id = 'a different id'

        self.assertNotEquals(question1, question2)
        self.assertNotEquals(question2, question1)

        question1.id = 'some-id'

        self.assertEquals(question1, question2)
        self.assertEquals(question2, question1)

        response1_1.id = 'a different id'

        self.assertNotEquals(question1, question2)
        self.assertNotEquals(question2, question1)

    def test_hashing(self):
        question1 = Question()

        question1.id = 'some-id'
        question1.title = 'my question object'
        question1.description = 'fill this in'

        question2 = Question()

        question2.id = 'some-id'
        question2.title = 'my question object'
        question2.description = 'fill this in'

        question_list = []

        question_list.append(question1)

        # Both objects areequivalent, so both appear to be in the list
        self.assertIn(question1, question_list)
        self.assertIn(question2, question_list)
        self.assertEquals(len(question_list), 1)

        question_list.append(question2)

        # Now they both are, but they are equivalent
        self.assertEquals(len(question_list), 2)

        question_set = set()

        question_set.add(question1)

        self.assertIn(question1, question_set)
        self.assertEquals(len(question_set), 1)

        question_set.add(question2)

        self.assertEquals(len(question_set), 1)
        self.assertIn(question1, question_set)
        self.assertIn(question2, question_set)

        question2.id = 'another-id'

        self.assertNotEquals(question1, question2)

        question_set.add(question2)

        self.assertEquals(len(question_set), 2)
        self.assertIn(question1, question_set)
        self.assertIn(question2, question_set)

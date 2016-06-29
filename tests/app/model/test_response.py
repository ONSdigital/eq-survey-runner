from app.model.answer import Answer
import unittest
import json


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

    def test_to_json(self):
        answer = Answer()

        answer.id = 'some-id'
        answer.label = 'my answer object'
        answer.guidance = 'fill this in'
        answer.type = 'some-type'
        answer.code = 'code'
        answer.messages['message1'] = "Message One"
        answer.messages['message2'] = "Message Two"

        # convert the dict to json, then into an dict again
        json_str = json.dumps(answer.to_json())
        json_obj = json.loads(json_str)

        # import pdb
        # pdb.set_trace()

        self.assertEquals(json_obj['id'], answer.id)
        self.assertEquals(json_obj['label'], answer.label)
        self.assertEquals(json_obj['guidance'], answer.guidance)
        self.assertEquals(json_obj['type'], answer.type)
        self.assertEquals(json_obj['q_code'], answer.code)
        self.assertIn("messages", json_obj['validation'])
        self.assertEquals(len(json_obj['validation']['messages']), 2)

    def test_equivalence(self):
        answer1 = Answer()

        answer1.id = 'some-id'
        answer1.label = 'my answer object'
        answer1.guidance = 'fill this in'
        answer1.type = 'some-type'
        answer1.code = 'code'
        answer1.messages['message1'] = "Message One"
        answer1.messages['message2'] = "Message Two"

        answer2 = Answer()

        answer2.id = 'some-id'
        answer2.label = 'my answer object'
        answer2.guidance = 'fill this in'
        answer2.type = 'some-type'
        answer2.code = 'code'
        answer2.messages['message1'] = "Message One"
        answer2.messages['message2'] = "Message Two"

        self.assertEquals(answer1, answer2)

        answer2.id = 'another-id'

        self.assertNotEquals(answer1, answer2)

        answer2.id = 'some-id'

        self.assertEquals(answer1, answer2)

        answer2.label = 'another answer object'

        self.assertNotEquals(answer1, answer2)

    def test_hashing(self):
        answers_list = []

        answer1 = Answer()
        answer2 = Answer()

        self.assertEquals(answer1, answer2)
        self.assertEquals(answer2, answer1)

        answers_list.append(answer1)

        self.assertEquals(len(answers_list), 1)

        answers_list.append(answer2)

        self.assertEquals(len(answers_list), 2)

        answer2.id = 'not answer1'

        self.assertNotEquals(answer1, answer2)
        self.assertNotEquals(answer2, answer1)

        answers_set = set()

        answers_set.add(answer1)

        self.assertEquals(len(answers_set), 1)

        answer2.id = None

        answers_set.add(answer2)

        self.assertEquals(len(answers_set), 1)
        self.assertIn(answer1, answers_set)
        self.assertIn(answer2, answers_set)

        answer2.id = 'different value'

        answers_set.add(answer2)

        self.assertEquals(len(answers_set), 2)
        self.assertIn(answer1, answers_set)
        self.assertIn(answer2, answers_set)

        self.assertNotEquals(answer1, answer2)

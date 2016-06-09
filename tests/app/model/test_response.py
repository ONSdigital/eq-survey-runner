from app.model.response import Response
import unittest
import json


class ResponseModelTest(unittest.TestCase):
    def test_basics(self):
        response = Response()

        response.id = 'some-id'
        response.label = 'my response object'
        response.guidance = 'fill this in'
        response.type = 'some-type'
        response.code = 'code'
        response.container = None

        self.assertEquals(response.id, 'some-id')
        self.assertEquals(response.label, 'my response object')
        self.assertEquals(response.guidance, 'fill this in')
        self.assertEquals(response.type, 'some-type')
        self.assertEquals(response.code, 'code')
        self.assertIsNone(response.container)

    def test_to_json(self):
        response = Response()

        response.id = 'some-id'
        response.label = 'my response object'
        response.guidance = 'fill this in'
        response.type = 'some-type'
        response.code = 'code'
        response.messages['message1'] = "Message One"
        response.messages['message2'] = "Message Two"

        # convert the dict to json, then into an dict again
        json_str = json.dumps(response.to_json())
        json_obj = json.loads(json_str)

        # import pdb
        # pdb.set_trace()

        self.assertEquals(json_obj['id'], response.id)
        self.assertEquals(json_obj['label'], response.label)
        self.assertEquals(json_obj['guidance'], response.guidance)
        self.assertEquals(json_obj['type'], response.type)
        self.assertEquals(json_obj['q_code'], response.code)
        self.assertIn("messages", json_obj['validation'])
        self.assertEquals(len(json_obj['validation']['messages']), 2)

    def test_equivalence(self):
        response1 = Response()

        response1.id = 'some-id'
        response1.label = 'my response object'
        response1.guidance = 'fill this in'
        response1.type = 'some-type'
        response1.code = 'code'
        response1.messages['message1'] = "Message One"
        response1.messages['message2'] = "Message Two"

        response2 = Response()

        response2.id = 'some-id'
        response2.label = 'my response object'
        response2.guidance = 'fill this in'
        response2.type = 'some-type'
        response2.code = 'code'
        response2.messages['message1'] = "Message One"
        response2.messages['message2'] = "Message Two"

        self.assertEquals(response1, response2)

        response2.id = 'another-id'

        self.assertNotEquals(response1, response2)

        response2.id = 'some-id'

        self.assertEquals(response1, response2)

        response2.label = 'another response object'

        self.assertNotEquals(response1, response2)

    def test_hashing(self):
        responses_list = []

        response1 = Response()
        response2 = Response()

        self.assertEquals(response1, response2)
        self.assertEquals(response2, response1)

        responses_list.append(response1)

        self.assertEquals(len(responses_list), 1)

        responses_list.append(response2)

        self.assertEquals(len(responses_list), 2)

        response2.id = 'not response1'

        self.assertNotEquals(response1, response2)
        self.assertNotEquals(response2, response1)

        responses_set = set()

        responses_set.add(response1)

        self.assertEquals(len(responses_set), 1)

        response2.id = None

        responses_set.add(response2)

        self.assertEquals(len(responses_set), 1)
        self.assertIn(response1, responses_set)
        self.assertIn(response2, responses_set)

        response2.id = 'different value'

        responses_set.add(response2)

        self.assertEquals(len(responses_set), 2)
        self.assertIn(response1, responses_set)
        self.assertIn(response2, responses_set)

        self.assertNotEquals(response1, response2)

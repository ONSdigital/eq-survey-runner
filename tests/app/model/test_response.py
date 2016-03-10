from app.model.response import Response
import unittest


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

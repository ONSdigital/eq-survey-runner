from app.responses.response_store import ResponseStore
from tests.app.framework.sr_unittest import SurveyRunnerTestCase
import unittest


class ResponseStoreTest(SurveyRunnerTestCase):

    def test_get_response(self):
        with self.application.test_request_context():
            response_store = ResponseStore()
            response_store.store_response("key1" , "test1")
            self.assertEquals("test1", response_store.get_response("key1"))


if __name__ == '__main__':
    unittest.main()

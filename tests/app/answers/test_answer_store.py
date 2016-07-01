from app.answers.answer_store import AnswerStore
from tests.app.framework.sr_unittest import SurveyRunnerTestCase
import unittest


class AnswerStoreTest(SurveyRunnerTestCase):

    def test_get_response(self):
        with self.application.test_request_context():
            answer_store = AnswerStore()
            answer_store.store_answer("key1" , "test1")
            self.assertEquals("test1", answer_store.get_answer("key1"))


if __name__ == '__main__':
    unittest.main()

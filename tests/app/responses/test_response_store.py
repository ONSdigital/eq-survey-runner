from app.responses.response_store import FlaskResponseStore
from flask import Flask
from datetime import timedelta
import unittest


class ResponseStoreTest(unittest.TestCase):

    def setUp(self):
        application = Flask(__name__)
        application.config['TESTING'] = True
        application.secret_key = 'you will not guess'
        application.permanent_session_lifetime = timedelta(seconds=1)
        self.application = application

    def test_get_response(self):
        with self.application.test_request_context():
            response_store = FlaskResponseStore()
            response_store.store_response("key1" , "test1")
            self.assertEquals("test1", response_store.get_response("key1"))


if __name__ == '__main__':
    unittest.main()

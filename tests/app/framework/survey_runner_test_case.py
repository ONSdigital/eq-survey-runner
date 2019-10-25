import unittest

from flask import Flask
from flask_login import LoginManager


login_manager = LoginManager()


class SurveyRunnerTestCase(unittest.TestCase):

    def setUp(self):
        application = Flask(__name__)
        application.config['TESTING'] = True
        application.secret_key = 'you will not guess'

        login_manager.init_app(application)
        self.application = application
        with self.application.test_client() as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'

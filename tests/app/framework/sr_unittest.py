import unittest
from app.authentication.user import User
from flask.ext.login import LoginManager
from datetime import timedelta
from flask import Flask

login_manager = LoginManager()

@login_manager.request_loader
def load_user(user_id):
    user = User("1")
    # clear any data
    user.delete_all()


class SurveyRunnerTestCase(unittest.TestCase):

    def setUp(self):
        application = Flask(__name__)
        application.config['TESTING'] = True
        application.secret_key = 'you will not guess'
        application.permanent_session_lifetime = timedelta(seconds=1)

        login_manager.init_app(application)
        self.application = application
        with self.application.test_client() as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'

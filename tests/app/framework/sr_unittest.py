import unittest
from app.authentication.user import User
from app.storage.storage_factory import StorageFactory
from flask_login import LoginManager
from datetime import timedelta
from flask import Flask

login_manager = LoginManager()


@login_manager.request_loader
def request_loader(request):
    user = User("1")
    return user


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

    def tearDown(self):
        with self.application.test_request_context():
            StorageFactory.get_storage_mechanism().clear()

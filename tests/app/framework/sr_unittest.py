import unittest
from app import settings
from app.authentication.user import User
from app.parser.v0_0_1.schema_parser import SchemaParser
from app.storage.storage_factory import get_storage
from flask_login import LoginManager
from datetime import timedelta
from flask import Flask
import os
import json

login_manager = LoginManager()


@login_manager.request_loader
def request_loader(request):
    user = User("1", "2")
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

        schema_file = open(os.path.join(settings.EQ_SCHEMA_DIRECTORY, "0_star_wars.json"))
        schema = schema_file.read()
        # create a parser
        self.schema_json = json.loads(schema)
        parser = SchemaParser(self.schema_json)
        self.questionnaire = parser.parse()

    def tearDown(self):
        with self.application.test_request_context():
            get_storage().clear()

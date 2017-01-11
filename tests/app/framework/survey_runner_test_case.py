import json
import os
import unittest
from datetime import timedelta

from flask import Flask
from flask_login import LoginManager

from app import settings
from app.parser.v0_0_1.schema_parser import SchemaParser

login_manager = LoginManager()


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
        self.user_id = "1"
        self.user_ik = "key"

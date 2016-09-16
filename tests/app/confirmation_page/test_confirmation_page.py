from app.routing.routing_engine import RoutingEngine
from app.parser.schema_parser_factory import SchemaParserFactory
from app.questionnaire.questionnaire_manager import QuestionnaireManager
import json
from app import settings
import unittest
import os


class TestConfirmationPage(unittest.TestCase):

    def setUp(self):
        schema_file = open(os.path.join(settings.EQ_SCHEMA_DIRECTORY, "0_rogue_one.json"))
        schema = schema_file.read()
        parser = SchemaParserFactory.create_parser(json.loads(schema))
        self.questionnaire = parser.parse()
        self.questionnaire_manager = QuestionnaireManager(self.questionnaire)
        self.routing_engine = RoutingEngine(self.questionnaire, self.questionnaire_manager)

    def test_get_next_location_confirmation(self):
        next_location = self.routing_engine.get_next_location('5e633f04-073a-44c0-a9da-a7cc2116b937')
        self.assertEqual('confirmation', next_location)

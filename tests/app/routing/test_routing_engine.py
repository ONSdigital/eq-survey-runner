from app.routing.routing_engine import RoutingEngine
from app.parser.schema_parser_factory import SchemaParserFactory
from app.questionnaire.questionnaire_manager import QuestionnaireManager
import json
from app import settings
import unittest
import os
from werkzeug.datastructures import MultiDict


class TestRoutingEngine(unittest.TestCase):

    def setUp(self):
        schema_file = open(os.path.join(settings.EQ_SCHEMA_DIRECTORY, "0_star_wars.json"))
        schema = schema_file.read()
        parser = SchemaParserFactory.create_parser(json.loads(schema))
        self.questionnaire = parser.parse()
        self.questionnaire_manager = QuestionnaireManager(self.questionnaire)
        self.routing_engine = RoutingEngine(self.questionnaire, self.questionnaire_manager)

    def test_get_next_location_introduction(self):
        next_location = self.routing_engine.get_next_location('introduction')
        self.assertEqual('f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0', next_location)

    def test_get_next_location_summary(self):
        next_location = self.routing_engine.get_next_location('an3b74d1-b687-4051-9634-a8f9ce10ard')
        self.assertEqual('846f8514-fed2-4bd7-8fb2-4b5fcb1622b1', next_location)

        next_location = self.routing_engine.get_next_location('846f8514-fed2-4bd7-8fb2-4b5fcb1622b1')
        self.assertEqual('summary', next_location)

    def test_routing_with_rules_with_when(self):
        current_block = 'f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0'
        user_answers = {'ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c': 'Dark Side'}
        next_location = self.update_questionnaire_manager(current_block, user_answers)
        self.assertEqual('923ccc84-9d47-4a02-8ebc-1e9d14fcf10b', next_location)

    def test_routing_with_rules_with_when_to_summary(self):
        current_block = 'f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0'
        user_answers = {'ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c': 'I prefer Star Trek'}
        next_location = self.update_questionnaire_manager(current_block, user_answers)
        self.assertEqual('summary', next_location)

    def test_routing_with_rules_without_when(self):
        current_block = 'fab02f02-6ce4-4f22-b61f-0c7880009f08'
        user_answers = {'a5d5ca1a-cf58-4626-be35-dce81297688b': 'Death Star'}
        next_location = self.update_questionnaire_manager(current_block, user_answers)
        self.assertEqual('cd3b74d1-b687-4051-9634-a8f9ce10a27d', next_location)

    def test_routing_with_no_rules(self):

        current_block = 'cd3b74d1-b687-4051-9634-a8f9ce10a27d'
        user_answers = MultiDict({
            "6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b": "234",
            "92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "40",
            "pre49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "1370",

            "a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d": "Elephant",
            "7587eb9b-f24e-4dc0-ac94-66118b896c10": "Luke, I am your father",
            "9587eb9b-f24e-4dc0-ac94-66117b896c10": ['Luke Skywalker', 'Yoda', 'Qui-Gon Jinn'],

            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "28",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "05",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "1983",

            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "29",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "05",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "1983"
        })

        next_location = self.update_questionnaire_manager(current_block, user_answers)
        self.assertEqual('an3b74d1-b687-4051-9634-a8f9ce10ard', next_location)

    def update_questionnaire_manager(self, current_block, user_answers):

        self.questionnaire_manager.go_to_state(current_block)
        self.questionnaire_manager.update_state(current_block, user_answers)

        next_location = self.routing_engine.get_next_location(current_block)
        return next_location

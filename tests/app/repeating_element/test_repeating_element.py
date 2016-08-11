from app.routing.routing_engine import RoutingEngine
from app.parser.schema_parser_factory import SchemaParserFactory
from app.questionnaire.questionnaire_manager import QuestionnaireManager
from app.routing.rules.repeating_element_rule import RepeatingElementRule
import json
from app import settings
import unittest
import os
from werkzeug.datastructures import MultiDict


class TestRepeatingElement(unittest.TestCase):

    def setUp(self):
        schema_file = open(os.path.join(settings.EQ_SCHEMA_DIRECTORY, "0_star_wars.json"))
        schema = schema_file.read()
        parser = SchemaParserFactory.create_parser(json.loads(schema))
        self.questionnaire = parser.parse()
        self.questionnaire_manager = QuestionnaireManager(self.questionnaire)
        self.routing_engine = RoutingEngine(self.questionnaire, self.questionnaire_manager)


    def test_repeating_elements_without_goto(self):

        current_block = '66cd681c-c3cb-4e32-8d51-b98337a6b524'

        user_answers = MultiDict({
            "8fe76762-d07f-4a1f-a315-0b0385940f8c": "3",
        })

        first_repetition = self.update_questionnaire_manager(current_block, user_answers)
        self.assertEqual('73ca315e-cab0-4b19-a79b-f850884db9e5_1', first_repetition)

        user_answers = MultiDict({
            "56b6f367-e84b-43fa-a5e2-19193f223fa0_1": "repetition 1",
        })

        second_repetition = self.update_questionnaire_manager(first_repetition, user_answers)
        self.assertEqual('73ca315e-cab0-4b19-a79b-f850884db9e5_2', second_repetition)

        user_answers = MultiDict({
            "56b6f367-e84b-43fa-a5e2-19193f223fa0_2": "repetition 2",
        })

        third_repetition = self.update_questionnaire_manager(second_repetition, user_answers)
        self.assertEqual('73ca315e-cab0-4b19-a79b-f850884db9e5_3', third_repetition)

        user_answers = MultiDict({
            "56b6f367-e84b-43fa-a5e2-19193f223fa0_3": "repetition 3",
        })

        fourth_page = self.update_questionnaire_manager(third_repetition, user_answers)
        self.assertEqual('cd3b74d1-b687-4051-9634-a8f9ce10a27d', fourth_page)

    def test_repeating_element_with_goto(self):

        current_block = '5ff0d900-530d-4266-8bed-c3d1f11b8d8c'

        user_answers = MultiDict({
            "50dd83c9-8de6-4c3b-be24-e85dd290b855": "1",
        })

        first_repetition = self.update_questionnaire_manager(current_block, user_answers)
        self.assertEqual('fab02f02-6ce4-4f22-b61f-0c7880009f08_1', first_repetition)

        user_answers = MultiDict({
            "a5d5ca1a-cf58-4626-be35-dce81297688b_1": "Death Star",
        })

        second_page = self.update_questionnaire_manager(first_repetition, user_answers)
        self.assertEqual('cd3b74d1-b687-4051-9634-a8f9ce10a27d', second_page)


    def update_questionnaire_manager(self, current_block, user_answers):

        self.questionnaire_manager.go_to_state(current_block)
        self.questionnaire_manager.update_state(current_block, user_answers)
        next_location = self.routing_engine.get_next_location(current_block)
        return next_location

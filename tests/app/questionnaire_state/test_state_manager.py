from app.questionnaire_state.state_manager import InMemoryStateManager
from app.questionnaire_state.user_journey_manager import UserJourneyManager
from app.parser.schema_parser_factory import SchemaParserFactory
from app import settings
import unittest
import os
import json


class TestDatabaseStateManager(unittest.TestCase):

    def setUp(self):

        schema_file = open(os.path.join(settings.EQ_SCHEMA_DIRECTORY, "0_star_wars.json"))
        schema = schema_file.read()
        # create a parser
        parser = SchemaParserFactory.create_parser(json.loads(schema))
        self.questionnaire = parser.parse()
        settings.EQ_SERVER_SIDE_STORAGE_TYPE = "IN_MEMORY"

    def test_store_and_retrieve(self):
        database_state_manager = InMemoryStateManager()

        # create the user journey manager
        user_journey_manager = UserJourneyManager(self.questionnaire)

        # add some state
        block1 = self.questionnaire.children[0].children[0]
        user_journey_manager.go_to_state(block1.id)
        user_answers = {}
        for section in block1.children:
            for question in section.children:
                for answer in question.children:
                      user_answers[answer.id] = "test"
        user_journey_manager.update_state(block1.id, user_answers)

        # save and retrieve it, checking the pickling works
        database_state_manager.save_state(user_journey_manager)

        self.assertEqual(user_journey_manager._schema.title, database_state_manager.get_state()._schema.title)
        self.assertEqual(user_journey_manager._schema.survey_id, database_state_manager.get_state()._schema.survey_id)
        self.assertEqual(user_journey_manager._schema.description, database_state_manager.get_state()._schema.description)
        self.assertEqual(user_journey_manager._current.item_id, database_state_manager.get_state()._current.item_id)
        self.assertEqual(user_journey_manager._first.item_id, database_state_manager.get_state()._first.item_id)
        self.assertEqual(len(user_journey_manager._archive), len(database_state_manager.get_state()._archive))

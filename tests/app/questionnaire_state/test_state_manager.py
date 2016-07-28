import json
import os
import unittest

from app import settings
from app.parser.schema_parser_factory import SchemaParserFactory
from app.questionnaire.state_manager import InMemoryStateManager
from app.questionnaire.questionnaire_manager import QuestionnaireManager
from werkzeug.datastructures from MultiDict


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

        # create the questionnaire manager
        questionnaire_manager = QuestionnaireManager(self.questionnaire)

        # add some state
        block1 = self.questionnaire.children[0].children[0]
        questionnaire_manager.go_to_state(block1.id)
        user_answers = MultiDict()
        for section in block1.children:
            for question in section.children:
                for answer in question.children:
                    user_answers[answer.id] = "test"
        questionnaire_manager.update_state(block1.id, user_answers)

        # save and retrieve it, checking the pickling works
        database_state_manager.save_state(questionnaire_manager)

        self.assertEqual(questionnaire_manager._schema.title, database_state_manager.get_state()._schema.title)
        self.assertEqual(questionnaire_manager._schema.survey_id, database_state_manager.get_state()._schema.survey_id)
        self.assertEqual(questionnaire_manager._schema.description, database_state_manager.get_state()._schema.description)
        self.assertEqual(questionnaire_manager._current.item_id, database_state_manager.get_state()._current.item_id)
        self.assertEqual(questionnaire_manager._first.item_id, database_state_manager.get_state()._first.item_id)
        self.assertEqual(len(questionnaire_manager._archive), len(database_state_manager.get_state()._archive))

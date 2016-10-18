import json
from unittest.mock import MagicMock, Mock

import os

from app import settings
from app.parser.schema_parser_factory import SchemaParserFactory
from app.questionnaire.questionnaire_manager import QuestionnaireManager
from app.questionnaire_state.node import Node
from app.schema.block import Block
from app.schema.group import Group
from app.schema.questionnaire import Questionnaire
from tests.app.framework.sr_unittest import SurveyRunnerTestCase


class TestQuestionnaireManager(SurveyRunnerTestCase):
    def setUp(self):
        super().setUp()
        schema_file = open(os.path.join(settings.EQ_SCHEMA_DIRECTORY, "0_star_wars.json"))
        schema = schema_file.read()
        # create a parser
        parser = SchemaParserFactory.create_parser(json.loads(schema))
        self.questionnaire = parser.parse()
        settings.EQ_SERVER_SIDE_STORAGE_TYPE = "IN_MEMORY"

    def test_get_state_is_none(self):
        questionnaire_manager = QuestionnaireManager(self.questionnaire)
        block1 = self.questionnaire.children[0].children[0]
        self.assertIsNone(questionnaire_manager.get_node(block1.id))

    def test_create_state(self):
        questionnaire_manager = QuestionnaireManager(self.questionnaire)
        block1 = self.questionnaire.children[0].children[0]
        questionnaire_manager.go_to_node(block1.id)
        self.assertIsNotNone(questionnaire_manager.get_node(block1.id))

    def test_append(self):
        questionnaire_manager = QuestionnaireManager(self.questionnaire)

        page1 = Node("first")
        page2 = Node("second")
        page3 = Node("third")

        self.assertIsNone(questionnaire_manager._tail)
        self.assertIsNone(questionnaire_manager._first)
        questionnaire_manager._append(page1)

        self.assertEqual(page1, questionnaire_manager._first)
        self.assertEqual(page1, questionnaire_manager._tail)
        self.assertIsNone(page1.previous)
        self.assertIsNone(page1.next)

        questionnaire_manager._append(page2)
        self.assertEqual(page1, questionnaire_manager._first)
        self.assertEqual(page2, questionnaire_manager._tail)
        self.assertIsNone(page1.previous)
        self.assertEqual(page1.next, page2)
        self.assertEqual(page2.previous, page1)
        self.assertIsNone(page2.next)

        questionnaire_manager._append(page3)
        self.assertEqual(page1, questionnaire_manager._first)
        self.assertEqual(page3, questionnaire_manager._tail)
        self.assertEqual(page2.previous, page1)
        self.assertEqual(page2.next, page3)
        self.assertEqual(page3.previous, page2)
        self.assertIsNone(page3.next)

    def test_pop(self):
        questionnaire_manager = QuestionnaireManager(self.questionnaire)

        page1 = Node("first")
        page2 = Node("second")
        page3 = Node("third")
        page4 = Node("fourth")

        questionnaire_manager._append(page1)
        questionnaire_manager._append(page2)
        questionnaire_manager._append(page3)
        questionnaire_manager._append(page4)

        self.assertEqual(page1, questionnaire_manager._first)
        self.assertEqual(page4, questionnaire_manager._tail)

        popped = questionnaire_manager._pop()
        self.assertEqual(page4, popped)
        self.assertIsNone(popped.previous)
        self.assertIsNone(popped.next)
        self.assertEqual(page3, questionnaire_manager._tail)
        self.assertIsNone(page3.next)

    def test_truncate(self):
        questionnaire_manager = QuestionnaireManager(self.questionnaire)

        page1 = Node("first")
        page2 = Node("second")
        page3 = Node("third")
        page4 = Node("fourth")

        questionnaire_manager._append(page1)
        questionnaire_manager._append(page2)
        questionnaire_manager._append(page3)
        questionnaire_manager._append(page4)

        self.assertEqual(page1, questionnaire_manager._first)
        self.assertEqual(page4, questionnaire_manager._tail)

        self.assertEqual(0, len(questionnaire_manager._archive))

        questionnaire_manager._truncate(page3)

        self.assertEqual(2, len(questionnaire_manager._archive))
        self.assertEqual(page4, questionnaire_manager._archive["fourth"])
        self.assertEqual(page3, questionnaire_manager._archive["third"])

        self.assertIsNone(page3.next)
        self.assertIsNone(page3.previous)

        self.assertIsNone(page4.next)
        self.assertIsNone(page4.previous)

        self.assertEqual(page2, questionnaire_manager._tail)
        self.assertIsNone(page2.next)

    def test_get_current_location(self):
        with self.application.test_request_context():
            schema = Questionnaire()
            group = Group()
            group.id = 'group-1'
            schema.register(group)
            block = Block()
            block.id = 'block-1'
            schema.register(block)
            group.add_block(block)
            schema.add_group(group)

            questionnaire_manager = QuestionnaireManager(schema)
            #  brand new session shouldn't have a current location
            self.assertEquals('block-1', questionnaire_manager.get_current_location())

    def test_get_current_location_with_intro(self):
        with self.application.test_request_context():
            schema = Questionnaire()
            schema.introduction = "anything"

            questionnaire_manager = QuestionnaireManager(schema)

            #  brand new session shouldn't have a current location
            self.assertEquals("introduction", questionnaire_manager.get_current_location())

    def test_go_to(self):
        with self.application.test_request_context():
            schema = Questionnaire()
            group = Group()
            group.id = 'group-1'
            schema.register(group)
            block = Block()
            block.id = 'block-1'
            schema.register(block)
            group.add_block(block)
            schema.add_group(group)

            questionnaire_manager = QuestionnaireManager(schema)

            questionnaire_manager.go_to_node("block-1")
            self.assertEquals("block-1", questionnaire_manager.get_current_location())

    def test_go_to_invalid_location(self):
        with self.application.test_request_context():
            schema = Questionnaire()
            group = Group()
            group.id = 'group-1'
            schema.register(group)
            block = Block()
            block.id = 'block-1'
            schema.register(block)
            group.add_block(block)
            schema.add_group(group)

            schema.introduction = {'description': 'Some sort of intro'}

            questionnaire_manager = QuestionnaireManager(schema)
            questionnaire_manager.go_to_node("introduction")
            self.assertEquals("introduction", questionnaire_manager.get_current_location())

    def test_update_node_answers_should_use_other_value_if_present(self):
        questionnaire_manager = QuestionnaireManager(self.questionnaire)

        mock_answer = MagicMock()
        mock_answer.id = 'answer id'
        mock_answer.other = 'other value'
        mock_answer.value = 'other'

        questionnaire_manager.state = Mock()
        questionnaire_manager.state.get_answers = MagicMock(return_value=[mock_answer])

        mock_node = MagicMock()
        questionnaire_manager.update_node_answers(mock_node)

        self.assertEquals(1, len(mock_node.answers))
        self.assertEquals({'answer id': 'other value'}, mock_node.answers)

    def test_update_node_answers_should_use_input_value_when_no_other_value(self):
        questionnaire_manager = QuestionnaireManager(self.questionnaire)

        mock_answer = MagicMock()
        mock_answer.id = 'answer id'
        mock_answer.other = None
        mock_answer.value = 'input value'

        questionnaire_manager.state = Mock()
        questionnaire_manager.state.get_answers = MagicMock(return_value=[mock_answer])

        mock_node = MagicMock()
        questionnaire_manager.update_node_answers(mock_node)

        self.assertEquals(1, len(mock_node.answers))
        self.assertEquals({'answer id': 'input value'}, mock_node.answers)

    def test_update_node_answers_returns_empty_dict_when_no_answers(self):
        questionnaire_manager = QuestionnaireManager(self.questionnaire)

        questionnaire_manager.state = Mock()
        questionnaire_manager.state.get_answers = MagicMock(return_value=[])

        mock_node = MagicMock()
        questionnaire_manager.update_node_answers(mock_node)

        self.assertEquals(0, len(mock_node.answers))
        self.assertEquals({}, mock_node.answers)

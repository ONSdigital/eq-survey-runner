import json
import os

from app import settings
from app.parser.schema_parser_factory import SchemaParserFactory
from app.questionnaire.state_manager import InMemoryStateManager
from app.questionnaire_state.page import Page
from app.questionnaire.questionnaire_manager import QuestionnaireManager
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

    def test_new_and_get_instance(self):
        # clear any state
        InMemoryStateManager.IN_MEMORY_STATE = {}

        # test there is no instance
        questionnaire_manager = QuestionnaireManager.get_instance()
        self.assertIsNone(questionnaire_manager)

        # test we can construct an instance
        questionnaire_manager = QuestionnaireManager.new_instance(self.questionnaire)
        self.assertIsNotNone(questionnaire_manager)

        # check get now returns one
        self.assertIsNotNone(QuestionnaireManager.get_instance())

    def test_get_state_is_none(self):
        questionnaire_manager = QuestionnaireManager(self.questionnaire)
        block1 = self.questionnaire.children[0].children[0]
        self.assertIsNone(questionnaire_manager.get_state(block1.id))

    def test_create_state(self):
        questionnaire_manager = QuestionnaireManager(self.questionnaire)
        block1 = self.questionnaire.children[0].children[0]
        questionnaire_manager.go_to_state(block1.id)
        self.assertIsNotNone(questionnaire_manager.get_state(block1.id))

    def test_update_state(self):
        questionnaire_manager = QuestionnaireManager(self.questionnaire)
        block1 = self.questionnaire.children[0].children[0]
        questionnaire_manager.go_to_state(block1.id)
        user_answers = {}
        for section in block1.children:
            for question in section.children:
                for answer in question.children:
                      user_answers[answer.id] = "test"
        questionnaire_manager.update_state(block1.id, user_answers)
        self.assertIsNotNone(questionnaire_manager.get_state(block1.id))

    def test_append(self):
        questionnaire_manager = QuestionnaireManager(self.questionnaire)

        page1 = Page("first", None)
        page2 = Page("second", None)
        page3 = Page("third", None)

        self.assertIsNone(questionnaire_manager._current)
        self.assertIsNone(questionnaire_manager._first)
        questionnaire_manager._append(page1)

        self.assertEqual(page1, questionnaire_manager._first)
        self.assertEqual(page1, questionnaire_manager._current)
        self.assertIsNone(page1.previous_page)
        self.assertIsNone(page1.next_page)

        questionnaire_manager._append(page2)
        self.assertEqual(page1, questionnaire_manager._first)
        self.assertEqual(page2, questionnaire_manager._current)
        self.assertIsNone(page1.previous_page)
        self.assertEqual(page1.next_page, page2)
        self.assertEqual(page2.previous_page, page1)
        self.assertIsNone(page2.next_page)

        questionnaire_manager._append(page3)
        self.assertEqual(page1, questionnaire_manager._first)
        self.assertEqual(page3, questionnaire_manager._current)
        self.assertEqual(page2.previous_page, page1)
        self.assertEqual(page2.next_page, page3)
        self.assertEqual(page3.previous_page, page2)
        self.assertIsNone(page3.next_page)

    def test_pop(self):
        questionnaire_manager = QuestionnaireManager(self.questionnaire)

        page1 = Page("first", None)
        page2 = Page("second", None)
        page3 = Page("third", None)
        page4 = Page("fourth", None)

        questionnaire_manager._append(page1)
        questionnaire_manager._append(page2)
        questionnaire_manager._append(page3)
        questionnaire_manager._append(page4)

        self.assertEqual(page1, questionnaire_manager._first)
        self.assertEqual(page4, questionnaire_manager._current)

        popped = questionnaire_manager._pop()
        self.assertEqual(page4, popped)
        self.assertIsNone(popped.previous_page)
        self.assertIsNone(popped.next_page)
        self.assertEqual(page3, questionnaire_manager._current)
        self.assertIsNone(page3.next_page)

    def test_truncate(self):
        questionnaire_manager = QuestionnaireManager(self.questionnaire)

        page1 = Page("first", None)
        page2 = Page("second", None)
        page3 = Page("third", None)
        page4 = Page("fourth", None)

        questionnaire_manager._append(page1)
        questionnaire_manager._append(page2)
        questionnaire_manager._append(page3)
        questionnaire_manager._append(page4)

        self.assertEqual(page1, questionnaire_manager._first)
        self.assertEqual(page4, questionnaire_manager._current)

        self.assertEqual(0, len(questionnaire_manager._archive))

        questionnaire_manager._truncate(page3)

        self.assertEqual(2, len(questionnaire_manager._archive))
        self.assertEqual(page4, questionnaire_manager._archive["fourth"])
        self.assertEqual(page3, questionnaire_manager._archive["third"])

        self.assertIsNone(page3.next_page)
        self.assertIsNone(page3.previous_page)

        self.assertIsNone(page4.next_page)
        self.assertIsNone(page4.previous_page)

        self.assertEqual(page2, questionnaire_manager._current)
        self.assertIsNone(page2.next_page)

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
            self.assertRaises(ValueError, questionnaire_manager.go_to_state, 'introduction')

            questionnaire_manager.go_to_state("block-1")
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
            questionnaire_manager.go_to_state("introduction")
            self.assertEquals("introduction", questionnaire_manager.get_current_location())

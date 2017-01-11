import json
import os
import unittest

from app.parser.v0_0_1.schema_parser import SchemaParser
from app.schema.answer import Answer
from app.schema.block import Block
from app.schema.group import Group
from app.schema.introduction import Introduction
from app.schema.question import Question
from app.schema.questionnaire import Questionnaire
from app.schema.section import Section


class TestSchemaParser(unittest.TestCase):

    @staticmethod
    def test_should_parse_questionnaire():
        # Load the json file as a dict
        schema_file = open(os.path.join(os.path.dirname(__file__), 'test_schemas/mci-mini.json'))
        schema = schema_file.read()
        schema = json.loads(schema)

        # create a parser
        parser = SchemaParser(schema)

        questionnaire = parser.parse()

        # Check the parser version
        assert parser.get_parser_version() == '0.0.1'

        # check the questionniare properties
        assert isinstance(questionnaire, Questionnaire)
        assert questionnaire.id == "22"
        assert questionnaire.survey_id == "23"
        assert questionnaire.title == "Monthly Business Survey - Retail Sales Index"
        assert questionnaire.description == "MCI description"
        assert len(questionnaire.groups) == 1
        assert isinstance(questionnaire.groups[0], Group)

    @staticmethod
    def test_should_parse_group():
        # Load the json file as a dict
        schema_file = open(os.path.join(os.path.dirname(__file__), 'test_schemas/mci-mini.json'))
        schema = schema_file.read()
        schema = json.loads(schema)

        # create a parser
        parser = SchemaParser(schema)
        questionnaire = parser.parse()

        # check the group properties
        assert len(questionnaire.groups) == 1
        assert isinstance(questionnaire.groups[0], Group)
        group = questionnaire.groups[0]

        assert group.id == "14ba4707-321d-441d-8d21-b8367366e766"
        assert group.title == ""

    @staticmethod
    def test_parse_block():
        # Load the json file as a dict
        schema_file = open(os.path.join(os.path.dirname(__file__), 'test_schemas/mci-mini.json'))
        schema = schema_file.read()
        schema = json.loads(schema)

        # create a parser
        parser = SchemaParser(schema)

        questionnaire = parser.parse()

        # check the block properties
        group = questionnaire.groups[0]
        block = group.blocks[0]
        assert len(group.blocks) == 1
        assert isinstance(group.blocks[0], Block)
        assert block.id == "cd3b74d1-b687-4051-9634-a8f9ce10a27d"
        assert block.title == "Monthly Business Survey"

    @staticmethod
    def test_should_parse_section():
        # Load the json file as a dict
        schema_file = open(os.path.join(os.path.dirname(__file__), 'test_schemas/mci-mini.json'))
        schema = schema_file.read()
        schema = json.loads(schema)

        # create a parser
        parser = SchemaParser(schema)
        questionnaire = parser.parse()

        # Check the parser version
        assert parser.get_parser_version() == '0.0.1'

        # check the section properties
        group = questionnaire.groups[0]
        block = group.blocks[0]
        section = block.sections[0]
        assert len(block.sections) == 1
        assert isinstance(block.sections[0], Section)
        assert section.id == "2cd99c83-186d-493a-a16d-17cb3c8bd302"
        assert section.title == ""

    @staticmethod
    def test_should_parse_question():
        # Load the json file as a dict
        schema_file = open(os.path.join(os.path.dirname(__file__), 'test_schemas/mci-mini.json'))
        schema = schema_file.read()
        schema = json.loads(schema)

        # create a parser
        parser = SchemaParser(schema)
        questionnaire = parser.parse()

        # check the question properties
        group = questionnaire.groups[0]
        block = group.blocks[0]
        section = block.sections[0]
        assert len(section.questions) == 2
        assert isinstance(section.questions[0], Question)
        question = section.questions[0]
        assert question.id == "4ba2ec8a-582f-4985-b4ed-20355deba55a"
        assert question.title == "On 12 January 2016 what was the number of employees for the business named above?"
        assert question.description == "An employee is anyone aged 16 years or over that your organisation directly " \
                                       "pays from its payroll(s), in return for carrying out a full-time or part-time " \
                                       "job or being on a training scheme."

    @staticmethod
    def test_should_parse_answer():
        # Load the json file as a dict
        schema_file = open(os.path.join(os.path.dirname(__file__), 'test_schemas/mci-mini.json'))
        schema = schema_file.read()
        schema = json.loads(schema)

        # create a parser
        parser = SchemaParser(schema)
        questionnaire = parser.parse()

        # Check the answer properties
        group = questionnaire.groups[0]
        block = group.blocks[0]
        section = block.sections[0]
        question = section.questions[0]
        assert len(question.answers) == 1
        assert isinstance(question.answers[0], Answer)
        answer = question.answers[0]
        assert answer.id == "29586b4c-fb0c-4755-b67d-b3cd398cb30a"
        assert answer.code == "110"
        assert answer.label == "Male employees working more than 30 hours per week?"
        assert answer.guidance == "How many men work for your company?"
        assert answer.type == "Integer"

        # check the answer properties on question 2
        question_two = section.questions[1]
        answer = question_two.answers[0]
        assert answer.type == "TextArea"

    def test_should_parse_introduction(self):
        # Load the json file as a dict
        schema_file = open(os.path.join(os.path.dirname(__file__), 'test_schemas/mci-mini-with-intro.json'))
        schema = schema_file.read()
        schema = json.loads(schema)

        # create a parser
        parser = SchemaParser(schema)
        questionnaire = parser.parse()

        # check the questionniare properties
        assert isinstance(questionnaire, Questionnaire)
        self.assertIsNotNone(questionnaire.introduction)
        self.assertIsInstance(questionnaire.introduction, Introduction)
        self.assertEqual(questionnaire.introduction.legal, "<b>This is the legal bit.</b>")
        self.assertEqual(questionnaire.introduction.description, "<p>This is the description.</p>")

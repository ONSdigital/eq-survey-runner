# -*- coding: utf-8 -*-
"""SchemaParser v0.0.1

This module defines the SchemaParser for the v0.0.1 of the survey schema

"""

from app.parser.abstract_schema_parser import AbstractSchemaParser
from app.parser.schema_parser_exception import SchemaParserException
from app.parser.parser_utils import ParserUtils

from app.model.questionnaire import Questionnaire
from app.model.group import Group
from app.model.block import Block
from app.model.section import Section
from app.model.question import Question
from app.model.response import Response
from app.model.display import Display
from app.model.properties import Properties

from app.model.introduction import Introduction

import logging


class SchemaParser(AbstractSchemaParser):
    """SchemaParser class

    Implements the inteface defined in the AbstractSchemaParser class

    """

    def __init__(self, schema):
        """Initialise the parser with the schema

        :param schema: the schema json object or dict

        """
        self._version = "0.0.1"
        self._schema = schema

    def get_parser_version(self):
        """Return which version of the parser

        :returns: The version number as a string, e.g. "0.0.1"

        """
        return self._version

    def parse(self):
        """Parse the schema

        :returns: A questionnaire object

        :raises: A SchemaParserException if there is a problem while parsing the schema

        """
        questionnaire = None

        try:
            questionnaire = Questionnaire()

            questionnaire.id = ParserUtils.get_required_string(self._schema, "questionnaire_id")
            questionnaire.title = ParserUtils.get_required_string(self._schema, "title")
            questionnaire.survey_id = ParserUtils.get_required_string(self._schema, "survey_id")
            questionnaire.description = ParserUtils.get_required_string(self._schema, "description")

        except Exception as e:
            logging.error('Error parsing schema')
            logging.info(e)
            raise e

        if questionnaire:
            if "introduction" in self._schema.keys():
                questionnaire.introduction = self._parse_introduction(self._schema['introduction'])

            if "groups" in self._schema.keys():
                for group_schema in self._schema['groups']:
                    questionnaire.add_group(self._parse_group(group_schema, questionnaire))
            else:
                raise SchemaParserException('Questionnaire must contain at least one group')

        return questionnaire

    def _parse_introduction(self, intro_schema):
        introduction = Introduction()

        introduction.legal = ParserUtils.get_optional_string(intro_schema, 'legal')
        introduction.description = ParserUtils.get_optional_string(intro_schema, 'description')

        return introduction

    def _parse_group(self, schema, questionnaire):
        """Parse a group element

        :param schema: The group schema

        :returns: Group object

        :raises: SchemaParserException

        """
        group = None

        try:
            group = Group()

            group.id = ParserUtils.get_required_string(schema, "id")
            group.title = ParserUtils.get_optional_string(schema, "title")

            # Register the group
            questionnaire.register(group)

        except Exception as e:
            logging.error('Error parsing schema')
            logging.info(e)
            raise e

        if "blocks" in schema.keys():
            for block_schema in schema['blocks']:
                group.add_block(self._parse_block(block_schema, questionnaire))
        else:
            raise SchemaParserException('Group must contain at least one block')

        return group

    def _parse_block(self, schema, questionnaire):
        """Parse a block element

        :param schema: The block schema

        :returns: A Block object

        :raises: SchemaParserException

        """
        block = Block()

        try:
            block.id = ParserUtils.get_required_string(schema, "id")
            block.title = ParserUtils.get_optional_string(schema, "title")

            # register the block
            questionnaire.register(block)

        except Exception as e:
            logging.error('Error parsing schema')
            logging.info(e)
            raise e

        if "sections" in schema.keys():
            for section_schema in schema['sections']:
                block.add_section(self._parse_section(section_schema, questionnaire))
        else:
            raise SchemaParserException('Block must contain at least one section')

        return block

    def _parse_section(self, schema, questionnaire):
        """Parse a section element

        :param schema: The section schema

        :returns: A Section object

        :raises: SchemaParserException

        """
        section = Section()

        try:
            section.id = ParserUtils.get_required_string(schema, "id")
            section.title = ParserUtils.get_optional_string(schema, "title")

            # regisger the section
            questionnaire.register(section)

        except Exception as e:
            logging.error('Error parsing schema')
            logging.info(e)
            raise e

        if 'questions' in schema.keys():
            for question_schema in schema['questions']:
                section.add_question(self._parse_question(question_schema, questionnaire))
        else:
            raise SchemaParserException('Section must have at least one question')

        return section

    def _parse_question(self, schema, questionnaire):
        """Parse a question element

        :param schema: The question schema

        :returns: A Question object

        :raises: SchemaParserException

        """
        question = Question()

        try:
            question.id = ParserUtils.get_required_string(schema, "id")
            question.title = ParserUtils.get_required_string(schema, "title")
            question.description = ParserUtils.get_required_string(schema, "description")
            question.type = ParserUtils.get_required_string(schema, "type")
            # register the question
            questionnaire.register(question)

        except Exception as e:
            logging.error('Error parsing schema')
            logging.info(e)
            raise e

        if 'responses' in schema.keys():
            for response_schema in schema['responses']:
                question.add_response(self._parse_response(response_schema, questionnaire))
        else:
            raise SchemaParserException('Question must contain at least one response')

        return question

    def _parse_response(self, schema, questionnaire):
        """Parse a response element

        :param schema: The response schema

        :returns: A Response object

        :raises: SchemaParserException

        """
        response = Response()

        try:
            response.id = ParserUtils.get_required_string(schema, 'id')
            response.code = ParserUtils.get_required_string(schema, 'q_code')
            response.label = ParserUtils.get_optional_string(schema, 'label')
            response.guidance = ParserUtils.get_optional_string(schema, 'guidance')
            response.type = ParserUtils.get_required_string(schema, 'type')
            response.mandatory = ParserUtils.get_required_boolean(schema, 'mandatory')

            display = ParserUtils.get_optional(schema, "display")
            if display:
                response.display = self._parse_display(display)

            if 'validation' in schema.keys():
                self._parse_validation(response, schema['validation'])

            # register the response
            questionnaire.register(response)

        except Exception as e:
            logging.error('Error parsing schema')
            logging.info(e)
            raise e

        return response

    def _parse_validation(self, response, schema):
        if 'messages' in schema.keys():
            messages = schema['messages']

            for code, message in messages.items():
                response.messages[code] = message

    def _parse_display(self, schema):
        """
        Parse a display element
        :param schema: the display element
        :return: A display object
        """
        display = Display()

        properties = ParserUtils.get_optional(schema, "properties")
        if properties:
            display.properties = self._parse_properties(properties)

        return display

    def _parse_properties(self, schema):
        """
         Parse a properties element
        :param schema: the properties element
        :return: a properties object
        """
        properties = Properties()

        try:
            properties.max_length = ParserUtils.get_optional_string(schema, 'max_length')

        except Exception as e:
            logging.error('Error parsing schema')
            logging.info(e)
            raise e

        return properties

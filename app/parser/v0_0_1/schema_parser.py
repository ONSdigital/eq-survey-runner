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
            logging.error(e)
            raise e

        if questionnaire:
            if "groups" in self._schema.keys():
                for group_schema in self._schema['groups']:
                    questionnaire.add_group(self._parse_group(group_schema))
            else:
                raise SchemaParserException('Questionnaire must contain at least one group')

        return questionnaire

    def _parse_group(self, schema):
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

        except Exception as e:
            logging.error(e)
            raise e

        if "blocks" in schema.keys():
            for block_schema in schema['blocks']:
                group.add_block(self._parse_block(block_schema))
        else:
            raise SchemaParserException('Group must contain at least one block')

        return group

    def _parse_block(self, schema):
        """Parse a block element

        :param schema: The block schema

        :returns: A Block object

        :raises: SchemaParserException

        """
        block = Block()

        try:
            block.id = ParserUtils.get_required_string(schema, "id")
            block.title = ParserUtils.get_optional_string(schema, "title")

        except Exception as e:
            logging.error(e)
            raise e

        if "sections" in schema.keys():
            for section_schema in schema['sections']:
                block.add_section(self._parse_section(section_schema))
        else:
            raise SchemaParserException('Block must contain at least one section')

        return block

    def _parse_section(self, schema):
        """Parse a section element

        :param schema: The section schema

        :returns: A Section object

        :raises: SchemaParserException

        """
        section = Section()

        try:
            section.id = ParserUtils.get_required_string(schema, "id")
            section.title = ParserUtils.get_optional_string(schema, "title")
        except Exception as e:
            logging.error(e)
            raise e

        if 'questions' in schema.keys():
            for question_schema in schema['questions']:
                section.add_question(self._parse_question(question_schema))
        else:
            raise SchemaParserException('Section must have at least one question')

        return section

    def _parse_question(self, schema):
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
        except Exception as e:
            logging.error(e)
            raise e

        if 'responses' in schema.keys():
            for response_schema in schema['responses']:
                question.add_response(self._parse_response(response_schema))
        else:
            raise SchemaParserException('Question must contain at least one response')

        return question

    def _parse_response(self, schema):
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
            response.required = ParserUtils.get_required_boolean(schema, 'required')
        except Exception as e:
            logging.error(e)
            raise e

        return response

# -*- coding: utf-8 -*-
"""SchemaParser v0.0.1

This module defines the SchemaParser for the v0.0.1 of the survey schema

"""


from app.parser.abstract_schema_parser import AbstractSchemaParser
from app.parser.schema_parser_exception import SchemaParserException


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

        :raises: A SchemaParserException if there is a problem while parsing the schema

        """
        if "groups" in self._schema.keys():
            for group_schema in self._schema['groups']:
                self._parse_group(group_schema)
        else:
            raise SchemaParserException('Questionnaire must contain at least one group')

    def _parse_group(self, schema):
        """Parse a group element

        :param schema: The group schema

        :raises: SchemaParserException

        """

        if "blocks" in schema.keys():
            for block_schema in schema['blocks']:
                self._parse_block(block_schema)
        else:
            raise SchemaParserException('Group must contain at least one block')

    def _parse_block(self, schema):
        """Parse a block element

        :param schema: The block schema

        :raises: SchemaParserException

        """

        if "sections" in schema.keys():
            for section_schema in schema['sections']:
                self._parse_section(section_schema)

    def _parse_section(self, schema):
        """Parse a section element

        :param schema: The section schema

        :raises: SchemaParserException

        """

        if 'questions' in schema.keys():
            for question_schema in schema['questions']:
                self._parse_question(question_schema)
        else:
            raise SchemaParserException('Section must have at least one question')

    @staticmethod
    def _parse_question(schema):
        """Parse a question element

        :param schema: The question schema

        :raises: SchemaParserException

        """
        if 'answers' not in schema.keys():
            raise SchemaParserException('Question must contain at least one answer')

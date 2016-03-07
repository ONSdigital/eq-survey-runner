from app.parser.schema_parser import SchemaParser as AbstractSchemaParser
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

    def __init__(self, schema):
        self._version = "0.0.1"
        self._schema = schema

    def get_parser_version(self):
        return self._version

    def parse(self):
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
                for groupSchema in self._schema['groups']:
                    questionnaire.add_group(self._parse_group(groupSchema))
            else:
                raise SchemaParserException('Questionnaire must contain at least one group')

        return questionnaire

    def _parse_group(self, schema):
        group = None

        try:
            group = Group()

            group.id = ParserUtils.get_required_string(schema, "id")
            group.title = ParserUtils.get_optional_string(schema, "title")

        except Exception as e:
            logging.error(e)
            raise e

        if "blocks" in schema.keys():
            for blockSchema in schema['blocks']:
                group.add_block(self._parse_block(blockSchema))
        else:
            raise SchemaParserException('Group must contain at least one block')

        return group

    def _parse_block(self, schema):
        block = Block()

        try:
            block.id = ParserUtils.get_required_string(schema, "id")
            block.title = ParserUtils.get_optional_string(schema, "title")

        except Exception as e:
            logging.error(e)
            raise e

        if "sections" in schema.keys():
            for sectionSchema in schema['sections']:
                block.add_section(self._parse_section(sectionSchema))
        else:
            raise SchemaParserException('Block must contain at least one section')

        return block

    def _parse_section(self, schema):
        section = Section()

        try:
            section.id = ParserUtils.get_required_string(schema, "id")
            section.title = ParserUtils.get_optional_string(schema, "title")
        except Exception as e:
            logging.error(e)
            raise e

        if 'questions' in schema.keys():
            for questionSchema in schema['questions']:
                section.add_question(self._parse_question(questionSchema))
        else:
            raise SchemaParserException('Section must have at least one question')

        return section

    def _parse_question(self, schema):
        question = Question()

        try:
            question.id = ParserUtils.get_required_string(schema, "id")
            question.title = ParserUtils.get_required_string(schema, "title")
            question.description = ParserUtils.get_required_string(schema, "description")
        except Exception as e:
            logging.error(e)
            raise e

        if 'responses' in schema.keys():
            for responseSchema in schema['responses']:
                question.add_response(self._parse_response(responseSchema))
        else:
            raise SchemaParserException('Question must contain at least one response')

        return question

    def _parse_response(self, schema):
        response = Response()

        try:
            response.id = ParserUtils.get_required_string(schema, 'id')
            response.code = ParserUtils.get_required_string(schema, 'q_code')
            response.label = ParserUtils.get_optional_string(schema, 'label')
            response.guidance = ParserUtils.get_optional_string(schema, 'guidance')
            response.type = ParserUtils.get_required_string(schema, 'type')
        except Exception as e:
            logging.error(e)
            raise e

        return response

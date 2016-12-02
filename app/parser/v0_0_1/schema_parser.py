# -*- coding: utf-8 -*-
"""SchemaParser v0.0.1

This module defines the SchemaParser for the v0.0.1 of the survey schema

"""
import copy

import logging

from app.parser.abstract_schema_parser import AbstractSchemaParser
from app.parser.parser_utils import ParserUtils
from app.parser.schema_parser_exception import SchemaParserException

from app.schema.answers.checkbox_answer import CheckboxAnswer
from app.schema.answers.currency_answer import CurrencyAnswer
from app.schema.answers.date_answer import DateAnswer
from app.schema.answers.integer_answer import IntegerAnswer
from app.schema.answers.month_year_date_answer import MonthYearDateAnswer
from app.schema.answers.percentage_answer import PercentageAnswer
from app.schema.answers.positiveinteger_answer import PositiveIntegerAnswer
from app.schema.answers.radio_answer import RadioAnswer
from app.schema.answers.relationship_answer import RelationshipAnswer
from app.schema.answers.textarea_answer import TextareaAnswer
from app.schema.answers.textfield_answer import TextfieldAnswer

from app.schema.block import Block
from app.schema.display import Display
from app.schema.group import Group
from app.schema.introduction import Introduction
from app.schema.properties import Properties
from app.schema.questionnaire import Questionnaire
from app.schema.questions.date_range_question import DateRangeQuestion
from app.schema.questions.general_question import GeneralQuestion
from app.schema.questions.relationship_question import RelationshipQuestion
from app.schema.questions.repeating_answer_question import RepeatingAnswerQuestion
from app.schema.section import Section
from app.schema.skip_condition import SkipCondition

from app.schema.when import When

from app.utilities.factory import Factory

logger = logging.getLogger(__name__)


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
        self.answer_factory = Factory()
        self.answer_factory.register_all({
            'CHECKBOX': CheckboxAnswer,
            'CURRENCY': CurrencyAnswer,
            'DATE': DateAnswer,
            'MONTHYEARDATE': MonthYearDateAnswer,
            'INTEGER': IntegerAnswer,
            'PERCENTAGE': PercentageAnswer,
            'POSITIVEINTEGER': PositiveIntegerAnswer,
            'RADIO': RadioAnswer,
            'TEXTAREA': TextareaAnswer,
            'TEXTFIELD': TextfieldAnswer,
            'RELATIONSHIP': RelationshipAnswer,
        })

        self.question_factory = Factory()
        self.question_factory.register_all({
            'GENERAL': GeneralQuestion,
            'DATERANGE': DateRangeQuestion,
            'REPEATINGANSWER': RepeatingAnswerQuestion,
            'RELATIONSHIP': RelationshipQuestion,
        })

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
        try:
            questionnaire = Questionnaire()
            questionnaire.id = ParserUtils.get_required_string(self._schema, "questionnaire_id")
            questionnaire.eq_id = ParserUtils.get_required_string(self._schema, "eq_id")
            logger.debug("eq_id: " + questionnaire.eq_id)
            questionnaire.title = ParserUtils.get_required_string(self._schema, "title")
            questionnaire.survey_id = ParserUtils.get_required_string(self._schema, "survey_id")
            logger.debug("title: " + questionnaire.title)
            questionnaire.description = ParserUtils.get_required_string(self._schema, "description")
            questionnaire.theme = ParserUtils.get_required_string(self._schema, "theme")
            questionnaire.submission_page = ParserUtils.get_optional_string(self._schema, "submission_page", questionnaire.submission_page)
            questionnaire.data_version = ParserUtils.get_required_string(self._schema, "data_version")

        except Exception as e:
            logging.error('Error parsing schema')
            logging.info(e)
            raise e

        if "introduction" in self._schema.keys():
            questionnaire.introduction = self._parse_introduction(self._schema['introduction'])

        if "groups" in self._schema.keys():
            for group_schema in self._schema['groups']:
                questionnaire.add_group(self._parse_group(group_schema, questionnaire))
        else:
            raise SchemaParserException('Questionnaire must contain at least one group')

        if 'messages' in self._schema.keys():
            # re-use the parse validation method
            self._parse_validation(questionnaire, self._schema)

        questionnaire.register_aliases()

        return questionnaire

    @staticmethod
    def _parse_introduction(intro_schema):
        introduction = Introduction()

        introduction.legal = ParserUtils.get_optional_string(intro_schema, 'legal')
        introduction.description = ParserUtils.get_optional_string(intro_schema, 'description')
        introduction.information_to_provide = ParserUtils.get_optional_array(intro_schema, 'information_to_provide')

        return introduction

    def _parse_group(self, schema, questionnaire):
        """Parse a group element

        :param schema: The group schema

        :returns: Group object

        :raises: SchemaParserException

        """
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
            block.type = ParserUtils.get_optional_string(schema, "type")
            block.routing_rules = ParserUtils.get_optional_array(schema, 'routing_rules')

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
            section.number = ParserUtils.get_optional_string(schema, "number")
            section.description = ParserUtils.get_optional_string(schema, "description")

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
        try:
            question_type = ParserUtils.get_required_string(schema, "type")
            question = self.question_factory.create(question_type.upper())
            question.type = question_type
            question.id = ParserUtils.get_required_string(schema, "id")
            question.title = ParserUtils.get_required_string(schema, "title")
            question.number = ParserUtils.get_optional_string(schema, "number")
            question.description = ParserUtils.get_optional_string(schema, "description")
            question.skip_condition = self._parse_skip_condition(ParserUtils.get_optional(schema, "skip_condition"))
            question.guidance = ParserUtils.get_optional(schema, "guidance")
            # register the question
            questionnaire.register(question)

        except Exception as e:
            logging.error('Error parsing schema')
            logging.info(e)
            raise e

        if 'answers' in schema.keys():
            for answer_schema in schema['answers']:
                question.add_answer(self._parse_answer(answer_schema, questionnaire))
        else:
            raise SchemaParserException('Question must contain at least one answer')

        return question

    @staticmethod
    def _parse_skip_condition(skip_condition_schema):
        if skip_condition_schema:
            skip_condition = SkipCondition()
            when_schema = ParserUtils.get_required(skip_condition_schema, "when")
            when = When()
            when.condition = ParserUtils.get_required(when_schema, 'condition')
            when.id = ParserUtils.get_optional(when_schema, 'id')
            when.meta = ParserUtils.get_optional(when_schema, 'meta')
            when.value = ParserUtils.get_required(when_schema, 'value')
            skip_condition.when = when
            return skip_condition
        else:
            return None

    def _parse_answer(self, schema, questionnaire):
        """Parse a answer element

        :param schema: The answer schema

        :returns: A Answer object

        :raises: SchemaParserException

        """
        try:
            answer_type = ParserUtils.get_required_string(schema, 'type')
            answer_id = ParserUtils.get_required_string(schema, 'id')
            answer = self.answer_factory.create(answer_type.upper(), answer_id)
            answer.type = answer_type
            answer.code = ParserUtils.get_required_string(schema, 'q_code')
            answer.label = ParserUtils.get_optional_string(schema, 'label')
            answer.guidance = ParserUtils.get_optional_string(schema, 'guidance')
            answer.mandatory = ParserUtils.get_required_boolean(schema, 'mandatory')
            answer.options = ParserUtils.get_optional_array(schema, 'options')
            answer.alias = ParserUtils.get_optional_string(schema, 'alias')
            display = ParserUtils.get_optional(schema, "display")
            if display:
                answer.display = self._parse_display(display)

            if 'validation' in schema.keys():
                self._parse_validation(answer, schema['validation'])

            # register the answer
            questionnaire.register(answer)

        except Exception as e:
            logging.error('Error parsing schema')
            logging.info(e)
            raise e

        return answer

    @staticmethod
    def _parse_validation(answer, schema):
        if 'messages' in schema.keys():
            messages = schema['messages']

            for code, message in messages.items():
                answer.messages[code] = message

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

    @staticmethod
    def _parse_properties(schema):
        """
         Parse a properties element
        :param schema: the properties element
        :return: a properties object
        """
        properties = Properties()

        try:
            properties.__dict__ = copy.deepcopy(schema)

        except Exception as e:
            logging.error('Error parsing schema')
            logging.info(e)
            raise e

        return properties

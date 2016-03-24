from app.renderer.renderer import Renderer
from app.validation.validation_store import AbstractValidationStore
from app.responses.response_store import AbstractResponseStore
from app.validation.validation_result import ValidationResult

from app.model.questionnaire import Questionnaire
from app.model.group import Group
from app.model.block import Block
from app.model.section import Section
from app.model.question import Question
from app.model.response import Response

from collections import OrderedDict

import unittest


class TestRenderer(unittest.TestCase):
    def setUp(self):
        self.validation_store = MockValidationStore()
        self.response_store = MockResponseStore()
        self.schema = self._create_schema()

        # The responses and the validation results are not related for the purposes of this test
        # The renderer simply combines these objects to create new objects for consumption
        # by the templates.  We are not testing validation here

        # Populate the response store
        self.response_store.store_response('response-1', 'One')
        self.response_store.store_response('response-2', 'Two')
        # We do not provide a response for response-3

        # Populate the validation store
        self.validation_store.store_result('response-1', ValidationResult(True))
        r2_result = ValidationResult(False)
        r2_result.errors.append('There is an error')
        r2_result.warnings.append('There is a warning')
        self.validation_store.store_result('response-2', r2_result)
        r3_result = ValidationResult(False)
        r3_result.errors.append('This is a required field')
        self.validation_store.store_result('response-3', r3_result)

    def test_augment_responses(self):
        # Instantiate the renderer using the pre-populated mock objects
        renderer = Renderer(self.schema, self.response_store, self.validation_store)

        # Get the response objects
        response_1 = self.schema.get_item_by_id('response-1')
        response_2 = self.schema.get_item_by_id('response-2')
        response_3 = self.schema.get_item_by_id('response-3')

        # Check the attributes do not exist
        with self.assertRaises(AttributeError):
            value = response_1.value
        with self.assertRaises(AttributeError):
            value = response_1.is_valid

        # Augment the responses
        renderer._augment_responses()

        # Check the model has been augmented correctly
        self.assertEquals(response_1.value, 'One')
        self.assertTrue(response_1.is_valid)
        self.assertEquals(len(response_1.errors), 0)
        self.assertEquals(len(response_1.warnings), 0)

        self.assertEquals(response_2.value, 'Two')
        self.assertFalse(response_2.is_valid)
        self.assertEquals(len(response_2.errors), 1)
        self.assertEquals(len(response_2.warnings), 1)
        self.assertEquals(response_2.errors[0], 'There is an error')
        self.assertEquals(response_2.warnings[0], 'There is a warning')

        self.assertIsNone(response_3.value)
        self.assertFalse(response_3.is_valid)
        self.assertEquals(len(response_3.errors), 1)
        self.assertEquals(len(response_3.warnings), 0)
        self.assertEquals(response_3.errors[0], 'This is a required field')

    def test_augment_questionnaire(self):
        # Instantiate the renderer using the pre-populated mock objects
        renderer = Renderer(self.schema, self.response_store, self.validation_store)

        # check the attributes do not exist
        with self.assertRaises(AttributeError):
            errors = self.schema.errors
        with self.assertRaises(AttributeError):
            warnings = self.schema.warnings

        # augment the questionnaire
        renderer._augment_questionnaire()

        # check the questionnaire has been augmented correctly
        self.assertIsInstance(self.schema.errors, OrderedDict, 'Errors should be an OrderedDict')
        self.assertIsInstance(self.schema.warnings, OrderedDict, 'Warnings should be an OrderedDict')

        self.assertListEqual(self.schema.errors['response-2'], ['There is an error'])
        self.assertListEqual(self.schema.errors['response-3'], ['This is a required field'])
        self.assertListEqual(self.schema.warnings['response-2'], ['There is a warning'])



    def _create_schema(self):
        questionnaire = Questionnaire()

        group = Group()
        group.id = 'group-1'
        questionnaire.add_group(group)
        questionnaire.register(group)

        block = Block()
        block.id = 'block-1'
        group.add_block(block)
        questionnaire.register(block)

        section = Section()
        section.id = 'section-1'
        block.add_section(section)
        questionnaire.register(section)

        question_1 = Question()
        question_1.id = 'question-1'
        section.add_question(question_1)
        questionnaire.register(question_1)

        response_1 = Response()
        response_1.id = 'response-1'
        question_1.add_response(response_1)
        questionnaire.register(response_1)

        question_2 = Question()
        question_2.id = 'question-2'
        section.add_question(question_2)
        questionnaire.register(question_2)

        response_2 = Response()
        response_2.id = 'response-2'
        question_2.add_response(response_2)
        questionnaire.register(response_2)

        response_3 = Response()
        response_3.id = 'response-3'
        question_2.add_response(response_3)
        questionnaire.register(response_3)

        return questionnaire


class MockValidationStore(AbstractValidationStore):
    def __init__(self):
        self._store = {}

    def store_result(self, key, value):
        self._store[key] = value

    def get_result(self, key):
        if key in self._store.keys():
            return self._store[key]
        else:
            return None


class MockResponseStore(AbstractResponseStore):
    def __init__(self):
        self._responses = {}

    def store_response(self, key, value):
        self._responses[key] = value

    def get_response(self, key):
        if key in self._responses.keys():
            return self._responses[key]
        else:
            return None

    def get_responses(self):
        return self._responses

    def clear(self):
        self._responses.clear()

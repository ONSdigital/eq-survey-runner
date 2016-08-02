from app.templating.template_pre_processor import TemplatePreProcessor
from app.validation.validation_result import ValidationResult
from app.metadata.metadata_store import MetaDataStore, MetaDataConstants
from app.authentication.user import User

from app.schema.questionnaire import Questionnaire
from app.schema.group import Group
from app.schema.block import Block
from app.schema.section import Section
from app.schema.question import Question
from app.schema.answer import Answer

from app.questionnaire_state.page import Page
from app.questionnaire_state.block import Block as StateBlock

from collections import OrderedDict

import unittest


class TestTemplatePreProcessor(unittest.TestCase):
    def setUp(self):
        self.schema = self._create_schema()
        self.user_journey_manager = MockUserJourneyManager()
        user = User("1", "2")
        jwt = {
            MetaDataConstants.USER_ID.claim_id: "1",
            MetaDataConstants.FORM_TYPE.claim_id: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetaDataConstants.EQ_ID.claim_id: "2",
            MetaDataConstants.PERIOD_ID.claim_id: "3",
            MetaDataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetaDataConstants.RU_REF.claim_id: "2016-04-04",
            MetaDataConstants.RU_NAME.claim_id: "Apple",
            MetaDataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        self.metadata = MetaDataStore.save_instance(user, jwt)

        # The answers and the validation results are not related for the purposes of this test
        # The pre_proc simply combines these objects to create new objects for consumption
        # by the templates.  We are not testing validation here

        # Populate the answer store
        self.user_journey_manager.store_answer('answer-1', 'One')
        self.user_journey_manager.store_answer('answer-2', 'Two')
        # We do not provide a answer for answer-3

    def test_augment_questionnaire(self):
        # Instantiate the pre_proc using the pre-populated mock objects
        pre_proc = TemplatePreProcessor(self.schema, self.user_journey_manager)
        pre_proc.initialize(self.metadata)

        # check the attributes do not exist
        with self.assertRaises(AttributeError):
            errors = self.schema.errors
        with self.assertRaises(AttributeError):
            warnings = self.schema.warnings

        # augment the questionnaire
        pre_proc._augment_questionnaire()

        # check the questionnaire has been augmented correctly
        self.assertIsInstance(self.schema.errors, OrderedDict, 'Errors should be an OrderedDict')
        self.assertIsInstance(self.schema.warnings, OrderedDict, 'Warnings should be an OrderedDict')

    def test_build_view_data(self):
        pre_proc = TemplatePreProcessor(self.schema, self.user_journey_manager)
        pre_proc.initialize(self.metadata)

        context = pre_proc.build_view_data()

        self.assertIn('meta', context.keys())
        self.assertIn('content', context.keys())
        self.assertIn('navigation', context.keys())

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

        answer_1 = Answer()
        answer_1.id = 'answer-1'
        question_1.add_answer(answer_1)
        questionnaire.register(answer_1)

        question_2 = Question()
        question_2.id = 'question-2'
        section.add_question(question_2)
        questionnaire.register(question_2)

        answer_2 = Answer()
        answer_2.id = 'answer-2'
        answer_2.mandatory = True
        question_2.add_answer(answer_2)
        questionnaire.register(answer_2)

        answer_3 = Answer()
        answer_3.id = 'answer-3'
        question_2.add_answer(answer_3)
        questionnaire.register(answer_3)

        return questionnaire


class MockUserJourneyManager(object):
    def __init__(self):
        self.submitted = None
        self.submitted_at = None
        self._answers = {}

    def store_answer(self, key, value):
        self._answers[key] = value

    def find_answer(self, key):
        if key in self._answers.keys():
            return self._answers[key]
        else:
            return None

    def get_answers(self):
        return self._answers

    def clear(self):
        self._answers.clear()

    def clear_answers(self):
        self.clear()

    def get_current_location(self):
        return 'current-location'

    def get_first_block(self):
        return 'block-1'

    def get_state(self, item_id):
        block_state = StateBlock('block-1')
        page = Page('block-1', block_state)
        return page

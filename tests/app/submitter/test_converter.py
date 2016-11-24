import json
import unittest

from app.parser.metadata_parser import parse_metadata
from app.schema.answer import Answer
from app.schema.block import Block
from app.schema.group import Group
from app.schema.question import Question
from app.schema.questionnaire import Questionnaire
from app.schema.section import Section
from app.submitter.converter import Converter
from tests.app.framework.sr_unittest import SurveyRunnerTestCase

EXPECTED_RESPONSE = json.loads("""
      {
        "type" : "uk.gov.ons.edc.eq:surveyresponse",
        "version" : "0.0.1",
        "origin" : "uk.gov.ons.edc.eq",
        "survey_id": "021",
        "collection":{
          "exercise_sid": "test-sid",
          "instrument_id": "0205",
          "period": "2016-02-01"
        },
        "submitted_at": "2016-03-07T15:28:05Z",
        "metadata": {
          "user_id": "789473423",
          "ru_ref": "432423423423"
        },
        "paradata": {},
        "data": {
          "001": "2016-01-01",
          "002": "2016-03-30"
        }
      }""")

JWT = {
  "user_id": "789473423",
  "form_type": "0205",
  "collection_exercise_sid": "test-sid",
  "eq_id": "1",
  "period_id": "2016-02-01",
  "period_str": "2016-01-01",
  "ref_p_start_date": "2016-02-02",
  "ref_p_end_date": "2016-03-03",
  "ru_ref": "432423423423",
  "ru_name": "Apple",
  "return_by": "2016-07-07"
}


class TestConverter(SurveyRunnerTestCase):
    def test_prepare_answers(self):
        with self.application.test_request_context():
            self.maxDiff = None

            metadata = parse_metadata(JWT)

            user_answer = {"ABC": "2016-01-01", "DEF": "2016-03-30"}

            answer_1 = Answer()
            answer_1.id = "ABC"
            answer_1.code = "001"

            answer_2 = Answer()
            answer_2.id = "DEF"
            answer_2.code = "002"

            question = Question()
            question.id = 'question-1'
            question.add_answer(answer_1)
            question.add_answer(answer_2)

            section = Section()
            section.add_question(question)

            block = Block()
            block.id = 'block-1'
            block.add_section(section)

            group = Group()
            group.id = 'group-1'
            group.add_block(block)

            questionnaire = Questionnaire()
            questionnaire.survey_id = "021"
            questionnaire.add_group(group)

            questionnaire.register(group)
            questionnaire.register(block)
            questionnaire.register(section)
            questionnaire.register(question)
            questionnaire.register(answer_1)
            questionnaire.register(answer_2)

            answer_object, submitted_at = Converter.prepare_answers(metadata, questionnaire, user_answer)

            self.assertEquals(EXPECTED_RESPONSE["type"], answer_object["type"])
            self.assertEquals(EXPECTED_RESPONSE["version"], answer_object["version"])
            self.assertEquals(EXPECTED_RESPONSE["origin"], answer_object["origin"])
            self.assertEquals(EXPECTED_RESPONSE["survey_id"], answer_object["survey_id"])
            self.assertEquals(EXPECTED_RESPONSE["collection"], answer_object["collection"])
            self.assertEquals(EXPECTED_RESPONSE["metadata"], answer_object["metadata"])
            self.assertEquals(EXPECTED_RESPONSE["paradata"], answer_object["paradata"])
            self.assertEquals(EXPECTED_RESPONSE["data"], answer_object["data"])

    def test_answer_with_zero(self):
        with self.application.test_request_context():
            self.maxDiff = None

            metadata = parse_metadata(JWT)

            user_answer = {"GHI": 0}

            answer = Answer()
            answer.id = "GHI"
            answer.code = "003"

            question = Question()
            question.id = 'question-2'
            question.add_answer(answer)

            section = Section()
            section.add_question(question)

            block = Block()
            block.id = 'block-1'
            block.add_section(section)

            group = Group()
            group.id = 'group-1'
            group.add_block(block)

            questionnaire = Questionnaire()
            questionnaire.survey_id = "021"
            questionnaire.add_group(group)
            questionnaire.register(question)
            questionnaire.register(answer)

            answer_object, submitted_at = Converter.prepare_answers(metadata, questionnaire, user_answer)

            # Check the converter correctly
            self.assertEquals("0", answer_object["data"]["003"])

    def test_answer_with_multiple_instances(self):
        with self.application.test_request_context():
            self.maxDiff = None

            metadata = parse_metadata(JWT)

            user_answer = {
                "GHI": 0,
                "GHI_1": 1,
                "GHI_2": 2,
            }

            answer = Answer()
            answer.id = "GHI"
            answer.code = "003"

            question = Question()
            question.id = 'question-2'
            question.add_answer(answer)

            section = Section()
            section.add_question(question)

            block = Block()
            block.id = 'block-1'
            block.add_section(section)

            group = Group()
            group.id = 'group-1'
            group.add_block(block)

            questionnaire = Questionnaire()
            questionnaire.survey_id = "021"
            questionnaire.add_group(group)
            questionnaire.register(question)
            questionnaire.register(answer)

            answer_object, submitted_at = Converter.prepare_answers(metadata, questionnaire, user_answer)
            # Check the converter correctly
            self.assertTrue('0' in answer_object["data"]["003"])
            self.assertTrue('1' in answer_object["data"]["003"])
            self.assertTrue('2' in answer_object["data"]["003"])

    def test_prepare_answers_for_answer_containing_underscore(self):
        with self.application.test_request_context():
            self.maxDiff = None

            metadata = parse_metadata(JWT)

            user_answer = {
                "full_name": 0,
                "full_name_1": 1,
                "full_name_2": 2,
            }

            answer = Answer()
            answer.id = "full_name"
            answer.code = "003"

            question = Question()
            question.id = 'question-2'
            question.add_answer(answer)

            section = Section()
            section.add_question(question)

            block = Block()
            block.id = 'block-1'
            block.add_section(section)

            group = Group()
            group.id = 'group-1'
            group.add_block(block)

            questionnaire = Questionnaire()
            questionnaire.survey_id = "021"
            questionnaire.add_group(group)
            questionnaire.register(question)
            questionnaire.register(answer)

            answer_object, submitted_at = Converter.prepare_answers(metadata, questionnaire, user_answer)
            # Check the converter correctly
            self.assertTrue('0' in answer_object["data"]["003"])
            self.assertTrue('1' in answer_object["data"]["003"])
            self.assertTrue('2' in answer_object["data"]["003"])

if __name__ == '__main__':
    unittest.main()

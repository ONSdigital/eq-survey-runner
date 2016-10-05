import json
import unittest

from app.parser.metadata_parser import MetadataParser, MetadataConstants
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
  MetadataConstants.USER_ID.claim_id: "789473423",
  MetadataConstants.FORM_TYPE.claim_id: "0205",
  MetadataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
  MetadataConstants.EQ_ID.claim_id: "1",
  MetadataConstants.PERIOD_ID.claim_id: "2016-02-01",
  MetadataConstants.PERIOD_STR.claim_id: "2016-01-01",
  MetadataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
  MetadataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
  MetadataConstants.RU_REF.claim_id: "432423423423",
  MetadataConstants.RU_NAME.claim_id: "Apple",
  MetadataConstants.RETURN_BY.claim_id: "2016-07-07"
}

class TestConverter(SurveyRunnerTestCase):
    def test_prepare_answers(self):
        with self.application.test_request_context():
            self.maxDiff = None

            metadata = MetadataParser.parse_token(JWT)

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

            metadata = MetadataParser.parse_token(JWT)

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

if __name__ == '__main__':
    unittest.main()

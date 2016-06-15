from app.model.questionnaire import Questionnaire
from app.model.section import Section
from app.model.group import Group
from app.model.block import Block
from app.model.question import Question
from app.model.response import Response
from app.authentication.user import User
from app.metadata.metadata_store import MetaDataStore, MetaDataConstants
from app.submitter.converter import Converter
from tests.app.framework.sr_unittest import SurveyRunnerTestCase

import unittest
import json

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


class TestConverter(SurveyRunnerTestCase):

    def test_prepare_responses(self):
        with self.application.test_request_context():
            self.maxDiff = None

            user = User("1", "2")

            jwt = {
                MetaDataConstants.USER_ID: "789473423",
                MetaDataConstants.FORM_TYPE: "0205",
                MetaDataConstants.COLLECTION_EXERCISE_SID: "test-sid",
                MetaDataConstants.EQ_ID: "1",
                MetaDataConstants.PERIOD_ID: "2016-02-01",
                MetaDataConstants.PERIOD_STR: "2016-01-01",
                MetaDataConstants.REF_P_START_DATE: "2016-02-02",
                MetaDataConstants.REF_P_END_DATE: "2016-03-03",
                MetaDataConstants.RU_REF: "432423423423",
                MetaDataConstants.RU_NAME: "Apple",
                MetaDataConstants.RETURN_BY: "2016-07-07"
            }

            metadata = MetaDataStore.save_instance(user, jwt)

            user_response = {"ABC": "2016-01-01", "DEF": "2016-03-30"}

            response_1 = Response()
            response_1.id = "ABC"
            response_1.code = "001"

            response_2 = Response()
            response_2.id = "DEF"
            response_2.code = "002"

            question = Question()
            question.id = 'question-1'
            question.add_response(response_1)
            question.add_response(response_2)

            section = Section()
            section.add_question(question)

            block = Block()
            block.id = 'block-1'
            block.add_section(section)

            group = Group()
            group.id = 'group-1'
            group.add_block(block)

            questionniare = Questionnaire()
            questionniare.survey_id = "021"
            questionniare.add_group(group)

            questionniare.register(group)
            questionniare.register(block)
            questionniare.register(section)
            questionniare.register(question)
            questionniare.register(response_1)
            questionniare.register(response_2)

            response_object, submitted_at = Converter.prepare_responses(user, metadata, questionniare, user_response)

            self.assertEquals(EXPECTED_RESPONSE["type"], response_object["type"])
            self.assertEquals(EXPECTED_RESPONSE["version"], response_object["version"])
            self.assertEquals(EXPECTED_RESPONSE["origin"], response_object["origin"])
            self.assertEquals(EXPECTED_RESPONSE["survey_id"], response_object["survey_id"])
            self.assertEquals(EXPECTED_RESPONSE["collection"], response_object["collection"])
            self.assertEquals(EXPECTED_RESPONSE["metadata"], response_object["metadata"])
            self.assertEquals(EXPECTED_RESPONSE["paradata"], response_object["paradata"])
            self.assertEquals(EXPECTED_RESPONSE["data"], response_object["data"])

if __name__ == '__main__':
    unittest.main()

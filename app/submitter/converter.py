from flask_login import current_user
import json
import logging
import datetime


logger = logging.getLogger(__name__)

TYPE = "uk.gov.ons.edc.eq:surveyresponse"
VERSION = "0.0.1"
ORIGIN = "uk.gov.ons.edc.eq"


class Converter(object):

  def prepare_responses(self, questionnaire, responses):
      response = {}
      response["type"] = TYPE
      response["version"] = VERSION
      response["origin"] = ORIGIN
      response["survey_id"] = questionnaire.survey_id
      collection = {}
      collection["exercise_sid"] = current_user.get_collection_exercise_sid()
      collection["period"] = current_user.get_period_id()
      response["collection"] = collection
      response["submitted_at"] = str(datetime.now())
      metadata = {}
      metadata["user_id"] = current_user.get_user_id()
      metadata["ru_ref"] = current_user.get_ru_ref()
      response["metadata"] = metadata

      logger.error(json.dumps(response))
      return json.dumps(response)



#   "{
#   "type" : "uk.gov.ons.edc.eq:surveyresponse",
#   "version" : "0.0.1",
#   "origin" : "uk.gov.ons.edc.eq",
#   "survey_id": "021",
#   "collection":{
#     "exercise_sid": "hfjdskf",
#     "instrument_id": "yui789",
#     "period": "2016-02-01"
#   },
#   "submitted_at": "2016-03-07T15:28:05Z",
#   "metadata": {
#     "user_id": "789473423",
#     "ru_ref": "432423423423"
#   },
#   "paradata": {},
#   "data": {
#     "001": "2016-01-01",
#     "002": "2016-03-30"
#   }
# }"

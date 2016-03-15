from flask import current_app
import json
import logging
import datetime
from app import settings

PARADATA_KEY = "paradata"

METADATA_KEY = "metadata"

RU_REF_KEY = "ru_ref"

USER_ID_KEY = "user_id"

SUBMITTED_AT_KEY = "submitted_at"

COLLECTION_KEY = "collection"

PERIOD_KEY = "period"

EXERCISE_SID_KEY = "exercise_sid"

INSTRUMENT_KEY = "instrument_id"

SURVEY_ID_KEY = "survey_id"

ORIGIN_KEY = "origin"

VERSION_KEY = "version"

TYPE_KEY = "type"

DATA_KEY = "data"

TYPE = "uk.gov.ons.edc.eq:surveyresponse"

VERSION = "0.0.1"

ORIGIN = "uk.gov.ons.edc.eq"

logger = logging.getLogger(__name__)


class Converter(object):

    @staticmethod
    def prepare_responses(user, questionnaire, responses):
        """
        Create the JSON response format for down stream processing

        :param questionnaire: the questionnaire model
        :param responses: the users responses
        :return: a JSON object in the following format:
          {
            "type" : "uk.gov.ons.edc.eq:surveyresponse",
            "version" : "0.0.1",
            "origin" : "uk.gov.ons.edc.eq",
            "survey_id": "021",
            "collection":{
              "exercise_sid": "hfjdskf",
              "instrument_id": "yui789",
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
          }
        """
        survey_id = questionnaire.survey_id
        data = {}

        for key in responses.keys():
            item = questionnaire.get_item_by_id(key)
            if item is not None:
                value = responses[key]
                data[item.code] = value

        metadata = {USER_ID_KEY: user.get_user_id(), RU_REF_KEY: user.get_ru_ref()}

        collection = {EXERCISE_SID_KEY: user.get_collection_exercise_sid(),
                      INSTRUMENT_KEY: user.get_form_type(),
                      PERIOD_KEY: user.get_period_id()}

        paradata = {}

        response = {TYPE_KEY: TYPE, VERSION_KEY: VERSION, ORIGIN_KEY: ORIGIN, SURVEY_ID_KEY: survey_id,
                    SUBMITTED_AT_KEY: datetime.datetime.now().strftime(settings.DATETIME_FORMAT),
                    COLLECTION_KEY: collection, METADATA_KEY: metadata,
                    PARADATA_KEY: paradata, DATA_KEY: data}

        return json.dumps(response)

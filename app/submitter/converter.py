import json
import logging

from datetime import datetime, timezone

from app import settings
from app.questionnaire_state.state_repeating_answer_question import extract_answer_instance_id


logger = logging.getLogger(__name__)


class SubmitterConstants(object):

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

    TX_ID = "tx_id"


class Converter(object):

    @staticmethod
    def prepare_answers(metadata_store, questionnaire, answers):
        """
        Create the JSON answer format for down stream processing

        :param metadata_store: the metadata store
        :param questionnaire: the questionnaire schema
        :param answers: the users answers as a dict of id/value
        :return: a JSON object in the following format:
          {
            "tx_id": "0f534ffc-9442-414c-b39f-a756b4adc6cb",
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
              "001": "01-01-2016",
              "002": "30-03-2016"
            }
          }
        """
        survey_id = questionnaire.survey_id
        data = {}

        for key in answers.keys():
            answer_id, _ = extract_answer_instance_id(key)
            item = questionnaire.get_item_by_id(answer_id)
            if item is not None:
                value = answers[key]
                if value is not None:
                    if item.code not in data:
                        data[item.code] = Converter._encode_value(value)
                    else:
                        if not isinstance(data[item.code], list):
                            list_answers = [data[item.code]]
                            data[item.code] = list_answers
                        data[item.code].append(Converter._encode_value(value))

        metadata = {SubmitterConstants.USER_ID_KEY: metadata_store['user_id'],
                    SubmitterConstants.RU_REF_KEY: metadata_store['ru_ref']}

        collection = {SubmitterConstants.EXERCISE_SID_KEY: metadata_store['collection_exercise_sid'],
                      SubmitterConstants.INSTRUMENT_KEY: metadata_store['form_type'],
                      SubmitterConstants.PERIOD_KEY: metadata_store['period_id']}

        paradata = {}
        submitted_at = datetime.now(timezone.utc)

        payload = {SubmitterConstants.TX_ID: metadata_store['tx_id'],
                   SubmitterConstants.TYPE_KEY: SubmitterConstants.TYPE,
                   SubmitterConstants.VERSION_KEY: SubmitterConstants.VERSION,
                   SubmitterConstants.ORIGIN_KEY: SubmitterConstants.ORIGIN,
                   SubmitterConstants.SURVEY_ID_KEY: survey_id,
                   SubmitterConstants.SUBMITTED_AT_KEY: submitted_at.isoformat(),
                   SubmitterConstants.COLLECTION_KEY: collection,
                   SubmitterConstants.METADATA_KEY: metadata,
                   SubmitterConstants.PARADATA_KEY: paradata,
                   SubmitterConstants.DATA_KEY: data}

        logging.debug("Converted answer ready for submission %s", json.dumps(payload))
        return payload, submitted_at

    @staticmethod
    def _encode_value(value):
        if isinstance(value, int):
            return str(value)
        elif isinstance(value, datetime):
            return value.strftime(settings.SDX_DATE_FORMAT)
        else:
            return value

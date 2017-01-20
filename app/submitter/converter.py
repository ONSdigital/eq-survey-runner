import logging
from collections import OrderedDict
from datetime import datetime, timezone

from app import settings
from app.helpers.multiple_choice_helper import MultipleChoiceHelper
from app.schema.answers.checkbox_answer import CheckboxAnswer

logger = logging.getLogger(__name__)


class DataVersionError(Exception):
    def __init__(self, version):
        super().__init__()
        self.version = version

    def __str__(self):
        return 'Data version {} not supported'.format(self.version)


def convert_answers(metadata, questionnaire, answer_store, routing_path):
    """
    Create the JSON answer format for down stream processing
    :param metadata: metadata for the questionnaire
    :param questionnaire: the questionnaire schema
    :param answer_store: the users answers
    :param routing_path: the path followed by the user when answering the questionnaire
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
        "data": {}
      }
    """
    survey_id = questionnaire.survey_id
    submitted_at = datetime.now(timezone.utc)
    payload = {
        'tx_id': metadata['tx_id'],
        'type': 'uk.gov.ons.edc.eq:surveyresponse',
        'version': questionnaire.data_version,
        'origin': 'uk.gov.ons.edc.eq',
        'survey_id': survey_id,
        'submitted_at': submitted_at.isoformat(),
        'collection': _build_collection(metadata),
        'metadata': _build_metadata(metadata),
    }
    if questionnaire.data_version == '0.0.2':
        payload['data'] = convert_answers_to_census_data(answer_store, routing_path)
    elif questionnaire.data_version == '0.0.1':
        payload['data'] = convert_answers_to_data(answer_store, questionnaire, routing_path)
    else:
        raise DataVersionError(questionnaire.data_version)

    logging.debug("Converted answer ready for submission: %s", metadata['tx_id'])
    return payload


def convert_answers_to_data(answer_store, questionnaire_schema, routing_path):
    """
    Convert answers into the data format below
    "data": {
          "001": "01-01-2016",
          "002": "30-03-2016"
        }
    :param answer_store: questionnaire answers
    :param questionnaire_schema: Schema of the questionnaire answers
    :param routing_path: the path followed in the questionnaire
    :return: data in a formatted form
    """
    data = OrderedDict()
    for location in routing_path:
        answers_in_block = answer_store.filter(location=location)

        for answer in answers_in_block:
            item = questionnaire_schema.get_item_by_id(answer['answer_id'])
            value = answer['value']

            if item is not None and value is not None:
                if not isinstance(item, CheckboxAnswer) or any('q_code' not in option for option in item.options):
                    data[item.code] = _get_answer_data(data, item.code, value)
                else:
                    data.update(_get_checkbox_answer_data(item, value))
    return data


def _get_answer_data(original_data, item_code, value):

    if item_code in original_data:
        data_to_return = original_data[item_code]
        if not isinstance(data_to_return, list):
            data_to_return = [data_to_return]
        data_to_return.append(_encode_value(value))

        return data_to_return
    return _encode_value(value)


def _get_checkbox_answer_data(checkboxes_with_qcode, value):

    checkbox_answer_data = OrderedDict()

    for user_answer in value:
        # find the option in the schema which matches the users answer
        option = next((option for option in checkboxes_with_qcode.options if option['value'] == user_answer), None)

        if option:
            if option['value'].lower() == 'other':
                # if the user has selected 'other' we need to find the value it refers to.
                # when non-mandatory, the other box value can be empty, in this case we just use its value
                checkbox_answer_data[option['q_code']] = MultipleChoiceHelper.find_other_value(value, checkboxes_with_qcode.options) \
                                         or option['value']
            else:
                checkbox_answer_data[option['q_code']] = user_answer

    return checkbox_answer_data


def convert_answers_to_census_data(answer_store, routing_path):
    """
    Convert answers into the data format below
    "data": [
        {
            "value": "Joe Bloggs",
            "block_id": "household-composition",
            "answer_id": "household-full-name",
            "group_id": "multiple-questions-group",
            "group_instance": 0,
            "answer_instance": 0
        },
        {
            "value": "Fred Flintstone",
            "block_id": "household-composition",
            "answer_id": "household-full-name",
            "group_id": "multiple-questions-group",
            "group_instance": 0,
            "answer_instance": 1
        },
        {
            "value": "Husband or wife",
            "block_id": "relationships",
            "answer_id": "who-is-related",
            "group_id": "household-relationships",
            "group_instance": 0,
            "answer_instance": 0
        }
    ]
    :param answer_store: questionnaire answers
    :param routing_path: the path followed in the questionnaire
    :return: data in a formatted form
    """
    data = []
    for location in routing_path:
        answers_in_block = answer_store.filter(location=location)
        data.extend(answers_in_block)
    return data


def _build_collection(metadata):
    return {
        'exercise_sid': metadata['collection_exercise_sid'],
        'instrument_id': metadata['form_type'],
        'period': metadata['period_id'],
    }


def _build_metadata(metadata):
    return {
        'user_id': metadata['user_id'],
        'ru_ref': metadata['ru_ref'],
    }


def _encode_value(value):
    if isinstance(value, int):
        return str(value)
    elif isinstance(value, datetime):
        return value.strftime(settings.SDX_DATE_FORMAT)
    else:
        return value

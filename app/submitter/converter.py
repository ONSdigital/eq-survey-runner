from collections import OrderedDict
from datetime import datetime, timezone

from structlog import get_logger

from app import settings
from app.helpers.schema_helper import SchemaHelper

logger = get_logger()


class DataVersionError(Exception):
    def __init__(self, version):
        super().__init__()
        self.version = version

    def __str__(self):
        return 'Data version {} not supported'.format(self.version)


def convert_answers(metadata, questionnaire_json, answer_store, routing_path, flushed=False):
    """
    Create the JSON answer format for down stream processing
    :param metadata: metadata for the questionnaire
    :param questionnaire_json: the questionnaire json
    :param answer_store: the users answers
    :param routing_path: the path followed by the user when answering the questionnaire
    :return: a JSON object in the following format:
      {
        "tx_id": "0f534ffc-9442-414c-b39f-a756b4adc6cb",
        "type" : "uk.gov.ons.edc.eq:surveyresponse",
        "version" : "0.0.1",
        "origin" : "uk.gov.ons.edc.eq",
        "survey_id": "021",
        "flushed": true|false
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
    survey_id = questionnaire_json['survey_id']
    submitted_at = datetime.now(timezone.utc)
    payload = {
        'tx_id': metadata['tx_id'],
        'type': 'uk.gov.ons.edc.eq:surveyresponse',
        'version': questionnaire_json['data_version'],
        'origin': 'uk.gov.ons.edc.eq',
        'survey_id': survey_id,
        'flushed': flushed,
        'submitted_at': submitted_at.isoformat(),
        'collection': _build_collection(metadata),
        'metadata': _build_metadata(metadata),
    }
    if questionnaire_json['data_version'] == '0.0.2':
        payload['data'] = convert_answers_to_census_data(answer_store, routing_path)
    elif questionnaire_json['data_version'] == '0.0.1':
        payload['data'] = convert_answers_to_data(answer_store, questionnaire_json, routing_path)
    else:
        raise DataVersionError(questionnaire_json['data_version'])

    logger.debug("converted answer ready for submission")
    return payload


def convert_answers_to_data(answer_store, questionnaire_json, routing_path):
    """
    Convert answers into the data format below
    "data": {
          "001": "01-01-2016",
          "002": "30-03-2016"
        }
    :param answer_store: questionnaire answers
    :param questionnaire_json: The survey json
    :param routing_path: the path followed in the questionnaire
    :return: data in a formatted form
    """
    data = OrderedDict()
    for location in routing_path:
        answers_in_block = answer_store.filter(location=location)
        block_json = SchemaHelper.get_block(questionnaire_json, location.block_id)
        answer_schema_list = SchemaHelper.get_answers_by_id_for_block(block_json)

        for answer in answers_in_block:
            answer_schema = answer_schema_list[answer['answer_id']]
            value = answer['value']

            if answer_schema is not None and value is not None and 'parent_answer_id' not in answer_schema:
                if answer_schema['type'] != 'Checkbox' or any('q_code' not in option for option in answer_schema['options']):
                    answer_data = _get_answer_data(data, answer_schema['q_code'], value)
                    if answer_data is not None:
                        data[answer_schema['q_code']] = answer_data
                else:
                    data.update(_get_checkbox_answer_data(answer_store, answer_schema, value))
    return data


def _get_answer_data(original_data, item_code, value):

    if item_code in original_data:
        data_to_return = original_data[item_code]
        if not isinstance(data_to_return, list):
            data_to_return = [data_to_return]
        data_to_return.append(_encode_value(value))

        return data_to_return
    return _encode_value(value)


def _get_checkbox_answer_data(answer_store, checkboxes_with_qcode, value):

    checkbox_answer_data = OrderedDict()

    for user_answer in value:
        # find the option in the schema which matches the users answer
        option = next((option for option in checkboxes_with_qcode['options'] if option['value'] == user_answer), None)

        if option:
            if 'child_answer_id' in option:
                filtered = answer_store.filter(answer_id=option['child_answer_id'], limit=1)

                # if the user has selected 'other' we need to find the value it refers to.
                # when non-mandatory, the other box value can be empty, in this case we just use its value
                checkbox_answer_data[option['q_code']] = filtered[0]['value'] if len(filtered) == 1 else option['value']
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
    elif isinstance(value, str) and value == '':
        return None
    else:
        return value

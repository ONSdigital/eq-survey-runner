from collections import OrderedDict
from datetime import datetime, timezone
from structlog import get_logger

logger = get_logger()


class DataVersionError(Exception):
    def __init__(self, version):
        super().__init__()
        self.version = version

    def __str__(self):
        return 'Data version {} not supported'.format(self.version)


def convert_answers(metadata, schema, answer_store, routing_path, flushed=False):
    """
    Create the JSON answer format for down stream processing
    :param metadata: metadata for the questionnaire
    :param schema: QuestionnaireSchema class with populated schema json
    :param answer_store: the users answers
    :param routing_path: the path followed by the user when answering the questionnaire
    :param flushed: True when system submits the users answers, False when user submits there own answers
    :return: a JSON object in the following format:
      {
        'tx_id': '0f534ffc-9442-414c-b39f-a756b4adc6cb',
        'type' : 'uk.gov.ons.edc.eq:surveyresponse',
        'version' : '0.0.1',
        'origin' : 'uk.gov.ons.edc.eq',
        'survey_id': '021',
        'flushed': true|false
        'collection':{
          'exercise_sid': 'hfjdskf',
          'instrument_id': 'yui789',
          'period': '2016-02-01'
        },
        'submitted_at': '2016-03-07T15:28:05Z',
        'metadata': {
          'user_id': '789473423',
          'ru_ref': '432423423423'
        },
        'data': {}
      }
    """
    survey_id = schema.json['survey_id']
    submitted_at = datetime.now(timezone.utc)
    payload = {
        'tx_id': metadata['tx_id'],
        'type': 'uk.gov.ons.edc.eq:surveyresponse',
        'version': schema.json['data_version'],
        'origin': 'uk.gov.ons.edc.eq',
        'survey_id': survey_id,
        'flushed': flushed,
        'submitted_at': submitted_at.isoformat(),
        'collection': _build_collection(metadata),
        'metadata': _build_metadata(metadata),
    }
    if 'case_id' in metadata and metadata['case_id']:
        payload['case_id'] = metadata['case_id']
    if 'case_ref' in metadata and metadata['case_ref']:
        payload['case_ref'] = metadata['case_ref']

    if schema.json['data_version'] == '0.0.2':
        payload['data'] = convert_answers_to_census_data(answer_store, schema, routing_path)
    elif schema.json['data_version'] == '0.0.1':
        payload['data'] = convert_answers_to_data(answer_store, schema, routing_path)
    else:
        raise DataVersionError(schema.json['data_version'])

    logger.debug('converted answer ready for submission')
    return payload


def convert_answers_to_data(answer_store, schema, routing_path):
    """
    Convert answers into the data format below
    'data': {
          '001': '01-01-2016',
          '002': '30-03-2016'
        }
    :param answer_store: questionnaire answers
    :param schema: QuestionnaireSchema class with popuated schema json
    :param routing_path: the path followed in the questionnaire
    :return: data in a formatted form
    """
    data = OrderedDict()
    for location in routing_path:
        answer_ids = schema.get_answer_ids_for_block(location.block_id)
        answers_in_block = answer_store.filter(answer_ids, location.group_instance)
        answer_schema_list = schema.get_answers_by_id_for_block(location.block_id)

        for answer in answers_in_block:
            answer_schema = answer_schema_list[answer['answer_id']]

            value = answer['value']

            if answer_schema is not None and value is not None and 'parent_answer_id' not in answer_schema:
                if answer_schema['type'] != 'Checkbox' or any('q_code' not in option for option in
                                                              answer_schema['options']):
                    if 'q_code' not in answer_schema:
                        continue

                    answer_data = _get_answer_data(data, answer_schema['q_code'], value)
                    if answer_data is not None:
                        data[answer_schema['q_code']] = _format_downstream_answer(answer_schema['type'], answer['value'], answer_data)
                else:
                    data.update(_get_checkbox_answer_data(answer_store, answer_schema, value))
    return data


def _format_downstream_answer(answer_type, answer_value, answer_data):
    if answer_type == 'Date':
        return datetime.strptime(answer_value, '%Y-%m-%d').strftime('%d/%m/%Y')

    if answer_type == 'MonthYearDate':
        return datetime.strptime(answer_value, '%Y-%m').strftime('%m/%Y')

    return answer_data


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
                filtered = answer_store.filter(answer_ids=[option['child_answer_id']])

                if filtered.count() > 1:
                    raise Exception('Multiple answers found for {}'.format(option['child_answer_id']))

                # if the user has selected 'other' we need to find the value it refers to.
                # when non-mandatory, the other box value can be empty, in this case we just use its value
                checkbox_answer_data[option['q_code']] = option['value']
            else:
                checkbox_answer_data[option['q_code']] = user_answer

    return checkbox_answer_data


def convert_answers_to_census_data(answer_store, schema, routing_path):
    """
    Convert answers into the data format below
    'data': [
        {
            'value': 'Joe Bloggs',
            'block_id': 'household-composition',
            'answer_id': 'household-full-name',
            'group_id': 'multiple-questions-group',
            'group_instance': 0,
            'answer_instance': 0
        },
        {
            'value': 'Fred Flintstone',
            'block_id': 'household-composition',
            'answer_id': 'household-full-name',
            'group_id': 'multiple-questions-group',
            'group_instance': 0,
            'answer_instance': 1
        },
        {
            'value': 'Husband or wife',
            'block_id': 'relationships',
            'answer_id': 'who-is-related',
            'group_id': 'household-relationships',
            'group_instance': 0,
            'answer_instance': 0
        }
    ]
    :param answer_store: questionnaire answers
    :param routing_path: the path followed in the questionnaire
    :return: data in a formatted form
    """
    data = []
    for location in routing_path:
        answer_ids = schema.get_answer_ids_for_block(location.block_id)
        answers_in_block = answer_store.filter(answer_ids, location.group_instance)
        data.extend(answers_in_block)
    return data


def _build_collection(metadata):
    return {
        'exercise_sid': metadata['collection_exercise_sid'],
        'instrument_id': metadata['form_type'],
        'period': metadata['period_id'],
    }


def _build_metadata(metadata):
    downstream_metadata = {
        'user_id': metadata['user_id'],
        'ru_ref': metadata['ru_ref'],
        'ref_period_start_date': metadata['ref_p_start_date'],
    }
    if metadata.get('ref_p_end_date'):
        downstream_metadata['ref_period_end_date'] = metadata['ref_p_end_date']

    return downstream_metadata


def _encode_value(value):
    if isinstance(value, str):
        if value == '':
            return None
        return value
    return str(value)


def convert_feedback(message, name, email, url, metadata, survey_id):
    """
    Create the JSON answer format for down stream processing
    :param metadata: metadata for the questionnaire
    :param feedback_json: the feedback json
    :param survey_id: the string representing the survey id
    :return: a JSON object in the following format:
      {
        'tx_id': '0f534ffc-9442-414c-b39f-a756b4adc6cb',
        'type' : 'uk.gov.ons.edc.eq:feedback',
        'version' : '0.0.1',
        'origin' : 'uk.gov.ons.edc.eq',
        'survey_id': '021',
        'collection':{
          'exercise_sid': 'hfjdskf',
          'instrument_id': 'yui789',
          'period': '201602'
        },
        'submitted_at': '2016-03-07T15:28:05Z',
        'metadata': {
          'user_id': '789473423',
          'ru_ref': '432423423423'
        },
        'data': {}
      }
    """
    submitted_at = datetime.now(timezone.utc)
    payload = {
        'tx_id': metadata['tx_id'],
        'type': 'uk.gov.ons.edc.eq:feedback',
        'version': '0.0.1',
        'origin': 'uk.gov.ons.edc.eq',
        'survey_id': survey_id,
        'submitted_at': submitted_at.isoformat(),
        'collection': _build_collection(metadata),
        'metadata': _build_metadata(metadata),
    }

    payload['data'] = {
        'message': message,
        'name': name,
        'email': email,
        'url': url,
    }

    return payload

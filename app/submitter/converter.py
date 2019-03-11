from datetime import datetime
from structlog import get_logger
from app.submitter.convert_payload_0_0_1 import convert_answers_to_payload_0_0_1
from app.submitter.convert_payload_0_0_2 import convert_answers_to_payload_0_0_2

logger = get_logger()


class DataVersionError(Exception):
    def __init__(self, version):
        super().__init__()
        self.version = version

    def __str__(self):
        return 'Data version {} not supported'.format(self.version)


def convert_answers(metadata, collection_metadata, schema, answer_store, routing_path, flushed=False):
    """
    Create the JSON answer format for down stream processing
    :param metadata: metadata for the questionnaire
    :param collection_metadata: Any metadata about the collection of the questionnaire
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
        'started_at': '2016-03-06T15:28:05Z',
        'submitted_at': '2016-03-07T15:28:05Z',
        'metadata': {
          'user_id': '789473423',
          'ru_ref': '432423423423'
        },
        'data': {}
      }
    """
    survey_id = schema.json['survey_id']
    submitted_at = datetime.utcnow()
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
        'case_id': metadata['case_id'],
    }
    if collection_metadata.get('started_at'):
        payload['started_at'] = collection_metadata['started_at']
    if metadata.get('case_id'):
        payload['case_id'] = metadata['case_id']
    if metadata.get('case_ref'):
        payload['case_ref'] = metadata['case_ref']

    if schema.json['data_version'] == '0.0.2':
        payload['data'] = convert_answers_to_payload_0_0_2(answer_store, schema, routing_path)
    elif schema.json['data_version'] == '0.0.1':
        payload['data'] = convert_answers_to_payload_0_0_1(metadata, answer_store, schema, routing_path)
    else:
        raise DataVersionError(schema.json['data_version'])

    logger.info('converted answer ready for submission')
    return payload


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
    }

    if metadata.get('ref_p_start_date'):
        downstream_metadata['ref_period_start_date'] = metadata['ref_p_start_date']
    if metadata.get('ref_p_end_date'):
        downstream_metadata['ref_period_end_date'] = metadata['ref_p_end_date']

    return downstream_metadata


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
    submitted_at = datetime.utcnow()
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

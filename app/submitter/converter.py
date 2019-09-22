from datetime import datetime
from structlog import get_logger
from app.submitter.convert_payload_0_0_1 import convert_answers_to_payload_0_0_1
from app.submitter.convert_payload_0_0_3 import convert_answers_to_payload_0_0_3

logger = get_logger()


class DataVersionError(Exception):
    def __init__(self, version):
        super().__init__()
        self.version = version

    def __str__(self):
        return 'Data version {} not supported'.format(self.version)


def convert_answers(schema, questionnaire_store, routing_path, flushed=False):
    """
    Create the JSON answer format for down stream processing in the following format:
    ```
      {
        'tx_id': '0f534ffc-9442-414c-b39f-a756b4adc6cb',
        'type' : 'uk.gov.ons.edc.eq:surveyresponse',
        'version' : '0.0.1',
        'origin' : 'uk.gov.ons.edc.eq',
        'survey_id': '021',
        'flushed': true|false
        'collection':{
          'exercise_sid': 'hfjdskf',
          'schema_name': 'yui789',
          'period': '2016-02-01'
        },
        'started_at': '2016-03-06T15:28:05Z',
        'submitted_at': '2016-03-07T15:28:05Z',
        'response_id': '1234567890123456',
        'questionnaire_id': '1234567890000000',
        'channel': 'RH',
        'metadata': {
          'user_id': '789473423',
          'ru_ref': '432423423423'
        },
        'data': [
            ...
        ],
      }
    ```

    Args:
        schema: QuestionnaireSchema instance with populated schema json
        questionnaire_store: EncryptedQuestionnaireStorage instance for accessing current questionnaire data
        routing_path: The full routing path followed by the user when answering the questionnaire
        flushed: True when system submits the users answers, False when submitted by user.
    Returns:
        Data payload
    """
    metadata = questionnaire_store.metadata
    collection_metadata = questionnaire_store.collection_metadata
    answer_store = questionnaire_store.answer_store
    list_store = questionnaire_store.list_store

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
        'response_id': metadata['response_id'],
        'questionnaire_id': metadata['questionnaire_id'],
    }

    if metadata.get('channel'):
        payload['channel'] = metadata['channel']
    if metadata.get('case_type'):
        payload['case_type'] = metadata['case_type']
    if metadata.get('region_code'):
        payload['region_code'] = metadata['region_code']
    if collection_metadata.get('started_at'):
        payload['started_at'] = collection_metadata['started_at']
    if metadata.get('case_id'):
        payload['case_id'] = metadata['case_id']
    if metadata.get('case_ref'):
        payload['case_ref'] = metadata['case_ref']

    if schema.json['data_version'] == '0.0.3':
        payload['data'] = {
            'answers': convert_answers_to_payload_0_0_3(
                answer_store, list_store, schema, routing_path
            ),
            'lists': list_store.serialise(),
        }
    elif schema.json['data_version'] == '0.0.1':
        payload['data'] = convert_answers_to_payload_0_0_1(
            metadata, answer_store, list_store, schema, routing_path
        )
    else:
        raise DataVersionError(schema.json['data_version'])

    logger.info('converted answer ready for submission')
    return payload


def _build_collection(metadata):
    return {
        'exercise_sid': metadata['collection_exercise_sid'],
        'schema_name': metadata['schema_name'],
        'period': metadata['period_id'],
    }


def _build_metadata(metadata):
    downstream_metadata = {'user_id': metadata['user_id'], 'ru_ref': metadata['ru_ref']}

    if metadata.get('ref_p_start_date'):
        downstream_metadata['ref_period_start_date'] = metadata['ref_p_start_date']
    if metadata.get('ref_p_end_date'):
        downstream_metadata['ref_period_end_date'] = metadata['ref_p_end_date']
    if metadata.get('display_address'):
        downstream_metadata['display_address'] = metadata['display_address']

    return downstream_metadata

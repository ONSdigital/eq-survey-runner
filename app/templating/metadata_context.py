from app.libs.utils import convert_tx_id
from app.templating.schema_context import json_and_html_safe


def build_metadata_context(metadata):
    """
    :param metadata: user metadata
    :return: metadata context
    """
    return {
        'eq_id': json_and_html_safe(metadata['eq_id']),
        'form_type': json_and_html_safe(metadata['form_type']),
        'ref_p_start_date': metadata.get('ref_p_start_date'),
        'ref_p_end_date': metadata.get('ref_p_end_date'),
        'employment_date': metadata.get('employment_date'),
        'region_code': json_and_html_safe(metadata.get('region_code')),
        'period_str': json_and_html_safe(metadata.get('period_str')),
        'return_by': metadata.get('return_by'),
        'collection_id': json_and_html_safe(metadata.get('collection_exercise_sid')),
        'tx_id': convert_tx_id(metadata['tx_id']),
        'ru_name': json_and_html_safe(metadata.get('ru_ref')),
        'name': json_and_html_safe(metadata.get('ru_name')),
        'trad_as': json_and_html_safe(metadata.get('trad_as'))
    }


def build_metadata_context_for_survey_completed(session_data):

    metadata_context = {
        'submitted_time': session_data.submitted_time,
        'tx_id': convert_tx_id(session_data.tx_id),
        'ru_ref': session_data.ru_ref
    }

    if session_data.period_str:
        metadata_context.update({'period_str': session_data.period_str})
    if session_data.ru_name:
        metadata_context.update({'ru_name': session_data.ru_name})

    return metadata_context

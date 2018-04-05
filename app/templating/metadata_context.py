from app.libs.utils import convert_tx_id
from app.templating.schema_context import json_and_html_safe


def build_metadata_context(metadata):
    """
    :param metadata: user metadata
    :return: metadata context
    """
    render_data = {
        'survey': _build_survey_meta(metadata),
        'respondent': _build_respondent_meta(metadata),
    }
    return render_data


def _build_respondent_meta(metadata):

    respondent_id = metadata.get('ru_ref')
    name = metadata.get('ru_name')
    trading_as = metadata.get('trad_as')

    respondent_meta = {
        'tx_id': convert_tx_id(metadata['tx_id']),
        'respondent_id': json_and_html_safe(respondent_id),
        'name': json_and_html_safe(name),
        'trading_as': json_and_html_safe(trading_as),
    }
    return respondent_meta


def _build_survey_meta(metadata):
    return {
        'return_by': metadata.get('return_by'),
        'start_date': metadata['ref_p_start_date'],
        'end_date': metadata.get('ref_p_end_date'),
        'employment_date': metadata.get('employment_date'),
        'region_code': json_and_html_safe(metadata.get('region_code')),
        'period_str': json_and_html_safe(metadata.get('period_str')),
        'eq_id': json_and_html_safe(metadata['eq_id']),
        'collection_id': json_and_html_safe(metadata.get('collection_exercise_sid')),
        'form_type': json_and_html_safe(metadata['form_type']),
    }


def build_metadata_context_for_survey_completed(session_data):
    return {
        'survey': {
            'period_str': session_data.period_str,
            'submitted_time': session_data.submitted_time
        },
        'respondent': {
            'tx_id': convert_tx_id(session_data.tx_id),
            'ru_name': session_data.ru_name,
            'ru_ref': session_data.ru_ref,
        },
    }

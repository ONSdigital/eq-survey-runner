from app.libs.utils import convert_tx_id
from app.templating.schema_context import json_and_html_safe
from app.templating.schema_context import build_schema_metadata
from app.utilities.schema import load_schema_from_metadata


def build_metadata_context(metadata):
    """
    Builds the metadata context using eq claims and schema defined metadata
    :param metadata: token metadata
    :return: metadata context
    """
    eq_context = {
        'eq_id': json_and_html_safe(metadata['eq_id']),
        'collection_id': json_and_html_safe(metadata['collection_exercise_sid']),
        'form_type': json_and_html_safe(metadata['form_type']),
        'ru_ref': json_and_html_safe(metadata['ru_ref']),
        'tx_id': json_and_html_safe(metadata['tx_id']),
    }

    schema = load_schema_from_metadata(metadata)

    eq_context.update(build_schema_metadata(metadata, schema))

    return eq_context


def build_metadata_context_for_survey_completed(session_data):

    metadata_context = {
        'submitted_time': session_data.submitted_time,
        'tx_id': convert_tx_id(session_data.tx_id),
        'ru_ref': session_data.ru_ref,
        'trad_as': session_data.trad_as,
        'account_service_url': session_data.account_service_url,
    }

    if session_data.period_str:
        metadata_context['period_str'] = session_data.period_str
    if session_data.ru_name:
        metadata_context['ru_name'] = session_data.ru_name

    return metadata_context

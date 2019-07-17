from app.libs.utils import convert_tx_id


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

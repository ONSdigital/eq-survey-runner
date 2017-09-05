from flask import current_app, session
from flask_login import current_user, logout_user

from app.globals import get_questionnaire_store
from app.utilities.schema import load_schema_from_metadata


def _remove_survey_session_data():
    current_app.eq['session_storage'].delete_session_from_db()
    current_app.eq['session_storage'].remove_user_ik()
    logout_user()


def end_session_with_schema_context(schema=None):
    if schema is None:
        questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)
        metadata = questionnaire_store.metadata
        schema = load_schema_from_metadata(metadata)

    _remove_survey_session_data()

    session['theme'] = schema['theme']
    session['survey_title'] = schema['title']

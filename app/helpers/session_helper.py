from flask import current_app
from flask_login import logout_user


def remove_survey_session_data():
    current_app.eq['session_storage'].delete_session_from_db()
    current_app.eq['session_storage'].remove_user_ik()
    logout_user()

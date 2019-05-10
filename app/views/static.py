from flask import Blueprint, current_app, render_template as flask_render_template
from structlog import get_logger

from app.globals import get_session_store
from app.utilities.schema import load_schema_from_session_data

logger = get_logger()

contact_blueprint = Blueprint(name='contact', import_name=__name__)


@contact_blueprint.route('/contact-us', methods=['GET'])
def contact():
    session = None
    survey_id = None
    session_store = get_session_store()

    if session_store:
        session = session_store.session_data
        schema = load_schema_from_session_data(session)
        survey_id = schema.json['survey_id']

    contact_template = flask_render_template('static/contact-us.html',
                                             session=session,
                                             survey_id=survey_id,
                                             analytics_ua_id=current_app.config['EQ_UA_ID'])
    return contact_template


@contact_blueprint.route('/cookies-privacy', methods=['GET'])
def legal():
    cookie_template = flask_render_template('static/cookies-privacy.html',
                                            analytics_ua_id=current_app.config['EQ_UA_ID'])
    return cookie_template

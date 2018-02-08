from flask import Blueprint, current_app
from flask_themes2 import render_theme_template

from app.globals import get_session_store
from app.utilities.schema import load_schema_from_params

from structlog import get_logger

logger = get_logger()

contact_blueprint = Blueprint(name='contact', import_name=__name__)


@contact_blueprint.route('/contact-us', methods=['GET'])
def contact():
    session = None
    survey_id = None
    session_store = get_session_store()

    if session_store:
        session = session_store.session_data
        schema = load_schema_from_params(session.eq_id, session.form_type)
        survey_id = schema.json['survey_id']

    contact_template = render_theme_template(theme='default',
                                             template_name='static/contact-us.html',
                                             session=session,
                                             survey_id=survey_id,
                                             analytics_ua_id=current_app.config['EQ_UA_ID'])
    return contact_template


@contact_blueprint.route('/cookies-privacy', methods=['GET'])
def legal():
    cookie_template = render_theme_template(theme='default',
                                            template_name='static/cookies-privacy.html',
                                            analytics_ua_id=current_app.config['EQ_UA_ID'])
    return cookie_template

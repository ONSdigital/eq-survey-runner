from flask import Blueprint, current_app, request, session as cookie_session
from flask_themes2 import render_theme_template
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

    contact_template = render_theme_template(theme=cookie_session.get('theme', 'default'),
                                             template_name='static/contact-us.html',
                                             session=session,
                                             survey_id=survey_id,
                                             analytics_gtm_id=current_app.config['EQ_GTM_ID'],
                                             analytics_gtm_env_id=current_app.config['EQ_GTM_ENV_ID'])
    return contact_template


@contact_blueprint.route('/cookies-privacy', methods=['GET'])
def legal():
    cookie_template = render_theme_template(theme=cookie_session.get('theme', 'default'),
                                            template_name='static/cookies-privacy.html',
                                            analytics_gtm_id=current_app.config['EQ_GTM_ID'],
                                            analytics_gtm_env_id=current_app.config['EQ_GTM_ENV_ID'])
    return cookie_template

@contact_blueprint.route('/cookies-settings', methods=['GET'])
def settings():
    ons_cookie_policy = request.cookies.get('ons_cookie_message_displayed')
    cookie_template = render_theme_template(theme=cookie_session.get('theme', 'default'),
                                            cookies=ons_cookie_policy,
                                            template_name='static/cookies-settings.html')
    return cookie_template

                                            # analytics_gtm_id=current_app.config['EQ_GTM_ID'],
                                            # analytics_gtm_env_id=current_app.config['EQ_GTM_ENV_ID'])

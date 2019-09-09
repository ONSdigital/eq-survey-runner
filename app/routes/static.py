from flask import Blueprint
from structlog import get_logger

from app.globals import get_session_store
from app.helpers.template_helper import render_template
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

    return render_template(
        template='static/contact-us', session=session, survey_id=survey_id
    )


@contact_blueprint.route('/cookies-privacy', methods=['GET'])
def legal():
    return render_template(template='static/cookies-privacy')

@contact_blueprint.route('/privacy', methods=['GET'])
def privacy():
    return render_template(template='static/privacy')

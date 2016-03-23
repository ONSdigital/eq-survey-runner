import logging
from flask import render_template, request
from flask_login import login_required, current_user
from app.main.views.root import _load_and_parse_schema
from app.main.views.root import _redirect_to_location
from app.questionnaire.create_questionnaire_manager import create_questionnaire_manager
from app.submitter.submitter import Submitter
from app.utilities.factory import factory
from .. import main_blueprint
from app.main import errors

logger = logging.getLogger(__name__)


@main_blueprint.route('/submission', methods=['GET', 'POST'])
@login_required
def submission():

    logger.debug("Requesting submission page")

    response_store = factory.create("response-store")
    responses = response_store.get_responses()
    schema = _load_and_parse_schema()

    if not schema:
            return errors.page_not_found()

    if request.method == 'POST':
        submitter = Submitter()
        submitted = submitter.send_responses(current_user, schema, responses)
        if submitted:
            return _redirect_to_location("submitted")
        else:
            return errors.internal_server_error()

    questionnaire_manager = create_questionnaire_manager()
    questionnaire_manager.process_incoming_responses(responses)
    render_data = questionnaire_manager.get_rendering_context()

    return render_template('submission.html', questionnaire=render_data, data={
        "survey_code": schema.survey_id,
        "period": current_user.get_period_str(),
        "respondent_id": current_user.get_ru_ref(),
    })
g

import logging
from flask import render_template, request, session
from flask_login import login_required, current_user
from app.main.views.root import load_and_parse_schema
from app.main.views.root import redirect_to_location
from app.questionnaire.create_questionnaire_manager import create_questionnaire_manager
from app.submitter.submitter import SubmitterFactory
from app.submitter.submission_failed import SubmissionFailedException
from app.submitter.converter import SubmitterConstants
from app.utilities.factory import factory
from app import settings
from .. import main_blueprint
from app.main import errors

logger = logging.getLogger(__name__)


@main_blueprint.route('/submission', methods=['GET', 'POST'])
@login_required
def submission():

    # Redirect to thank you page if the questionnaire has already been submitted
    if SubmitterConstants.SUBMITTED_AT_KEY in session:
        return redirect_to_location("submitted")

    logger.debug("Requesting submission page")

    response_store = factory.create("response-store")
    responses = response_store.get_responses()
    questionnaire_manager = create_questionnaire_manager()
    schema = load_and_parse_schema()

    if not schema:
        return errors.page_not_found()

    if request.method == 'POST':
        # Check the responses are still valid
        questionnaire_manager.process_incoming_responses(responses)
        current_location = questionnaire_manager.get_current_location()

        if not responses or current_location == 'questionnaire':
            return redirect_to_location('questionnaire')

        submitter = SubmitterFactory.get_submitter()
        try:
            submitted_at = submitter.send_responses(current_user, schema, responses)
            # TODO I don't like this but until we sort out the landing/review/submission flow this is the easiest way
            session[SubmitterConstants.SUBMITTED_AT_KEY] = submitted_at.strftime(settings.DISPLAY_DATETIME_FORMAT)
            response_store.clear_responses()
            return redirect_to_location("submitted")
        except SubmissionFailedException as e:
            return errors.internal_server_error(e)

    render_data = questionnaire_manager.get_rendering_context()

    return render_template('submission.html', questionnaire=render_data, data={
        "survey_code": schema.survey_id,
        "period_str": current_user.get_period_str(),
        "respondent_id": current_user.get_ru_ref()
    }, bar_title=schema.title)

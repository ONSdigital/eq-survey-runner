import logging
from flask import render_template, request, session
from flask_login import login_required, current_user
from app.main.views.root import redirect_to_location
from app.questionnaire.create_questionnaire_manager import create_questionnaire_manager
from app.submitter.converter import SubmitterConstants
from .. import main_blueprint

logger = logging.getLogger(__name__)


@main_blueprint.route('/questionnaire', methods=['GET', 'POST'])
@login_required
def questionnaire():

    logger.debug("Current user %s", current_user)

    # Redirect to thankyou page if the questionnaire has already been submitted
    if SubmitterConstants.SUBMITTED_AT_KEY in session:
        return redirect_to_location("submitted")

    questionnaire_manager = create_questionnaire_manager()

    if request.method == 'POST':
        questionnaire_manager.process_incoming_responses(request.form)
        current_location = questionnaire_manager.get_current_location()
        logger.debug("POST request question - current location %s", current_location)

        return redirect_to_location(current_location)

    render_data = questionnaire_manager.get_rendering_context()

    schema = questionnaire_manager.get_schema()
    return render_template('questionnaire.html', questionnaire=render_data, data={
        "survey_code": schema.survey_id,
        "period_str": current_user.get_period_str(),
        "respondent_id": current_user.get_ru_ref()
    }, bar_title=schema.title)

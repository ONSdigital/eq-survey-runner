from flask import render_template, session
from flask_login import login_required, current_user
from .. import main_blueprint
import logging
from app.submitter.converter import SubmitterConstants
from app.main.views.root import load_and_parse_schema
from app.main import errors

logger = logging.getLogger(__name__)


@main_blueprint.route('/thank-you', methods=['GET'])
@login_required
def thank_you():
    logger.debug("Requesting thank you page")

    # load the schema
    schema = load_and_parse_schema()

    if not schema:
        return errors.page_not_found()

    # TODO this should be part of the navigation store really
    submitted_at = session[SubmitterConstants.SUBMITTED_AT_KEY]

    return render_template('thank-you.html', data={
        "survey_code": schema.survey_id,
        "period_str": current_user.get_period_str(),
        "respondent_id": current_user.get_ru_ref(),
        "submitted_at": submitted_at
    })

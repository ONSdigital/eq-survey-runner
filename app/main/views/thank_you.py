from flask import render_template
from flask_login import login_required, current_user
from .. import main_blueprint
import logging
from app.main.views.root import _load_and_parse_schema

logger = logging.getLogger(__name__)


@main_blueprint.route('/thank-you', methods=['GET'])
@login_required
def thank_you():
    logger.debug("Requesting thank you page")

    # load the schema
    schema = _load_and_parse_schema()

    return render_template('thank-you.html', data={
        "survey_code": schema.survey_id,
        "period": current_user.get_period_str(),
        "respondent_id": current_user.get_ru_ref(),
    })

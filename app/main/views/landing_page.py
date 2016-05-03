from flask import render_template, session
from flask_login import login_required
from .. import main_blueprint
import logging
from app.main.views.root import load_and_parse_schema, redirect_to_location
from app.submitter.converter import SubmitterConstants
from app.utilities.factory import factory
from datetime import datetime


logger = logging.getLogger(__name__)


@main_blueprint.route('/landing-page', methods=['GET', 'POST'])
@login_required
def landing_page():
    # Redirect to thank you page if the questionnaire has already been submitted
    if SubmitterConstants.SUBMITTED_AT_KEY in session:
        return redirect_to_location("submitted")

    logger.debug("Requesting landing page")

    metadata = factory.create("metadata-store")

    eq_id = metadata.get_eq_id()
    form_type = metadata.get_form_type()
    logger.debug("Requested questionnaire %s for form type %s", eq_id, form_type)

    schema = load_and_parse_schema(eq_id, form_type)

    return render_template('landing-page.html', data={
        "legal": schema.introduction.legal,
        "description": schema.introduction.description,
        "address": {
            "name": metadata.get_ru_name(),
            "trading_as": metadata.get_trad_as()
        },
        "survey_code": schema.survey_id,
        "period_str": metadata.get_period_str(),
        "respondent_id": metadata.get_ru_ref(),
        # You'd think there would be an easier way of doing this...
        "return_by": '{dt.day} {dt:%B} {dt.year}'.format(dt=datetime.strptime(metadata.get_return_by(), "%Y-%m-%d")),
        "start_date": '{dt.day} {dt:%B} {dt.year}'.format(dt=datetime.strptime(metadata.get_ref_p_start_date(), "%Y-%m-%d")),
        "end_date": '{dt.day} {dt:%B} {dt.year}'.format(dt=datetime.strptime(metadata.get_ref_p_end_date(), "%Y-%m-%d")),
        "title": schema.title
    }, bar_title=schema.title)

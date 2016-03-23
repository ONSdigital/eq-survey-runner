from flask import render_template
from flask_login import login_required, current_user
from .. import main_blueprint
import logging
from app.main.views.root import load_and_parse_schema


logger = logging.getLogger(__name__)


@main_blueprint.route('/cover-page', methods=['GET', 'POST'])
@login_required
def cover_page():
    logger.debug("Requesting cover page")
    eq_id = current_user.get_eq_id()
    form_type = current_user.get_form_type()
    logger.debug("Requested questionnaire %s for form type %s", eq_id, form_type)

    questionnaire = load_and_parse_schema()

    return render_template('cover-page.html', data={
        "legal": questionnaire.introduction.legal,
        "description": questionnaire.introduction.description,
        "address": {
            "name": current_user.get_ru_name()
        },
        "survey_code": questionnaire.survey_id,
        "period": current_user.get_period_str(),
        "respondent_id": current_user.get_ru_ref(),
        "return_by": current_user.get_return_by(),
        "start_date": current_user.get_ref_p_start_date(),
        "end_date": current_user.get_ref_p_end_date()
    })

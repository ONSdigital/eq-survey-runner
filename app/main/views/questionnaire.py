import logging


from app.data_model.questionnaire_store import get_metadata
from app.questionnaire.questionnaire_manager import InvalidLocationException
from app.questionnaire.questionnaire_manager_factory import QuestionnaireManagerFactory

from flask import redirect
from flask import request

from flask_login import current_user
from flask_login import login_required

from flask_themes2 import render_theme_template

from .. import main_blueprint

logger = logging.getLogger(__name__)


@main_blueprint.route('/questionnaire/<eq_id>/<form_type>/<period_id>/<collection_id>/<location>', methods=["GET"])
@login_required
def get_questionnaire(eq_id, form_type, period_id, collection_id, location):
    logger.debug("Get location : /questionnaire/%s/%s/%s/%s/%s", eq_id, form_type, period_id, collection_id, location)
    questionnaire_manager = QuestionnaireManagerFactory.get_instance()
    try:
        if not same_survey(collection_id, eq_id, form_type, period_id):
            return redirect("/information/multiple-surveys")
        elif questionnaire_manager.submitted:
            return do_redirect(eq_id, form_type, period_id, collection_id, 'thank-you')

        return render_page(location, questionnaire_manager)
    except InvalidLocationException:
        return do_redirect(eq_id, form_type, period_id, collection_id, questionnaire_manager.get_current_location())


@main_blueprint.route('/questionnaire/<eq_id>/<form_type>/<period_id>/<collection_id>/<location>', methods=["POST"])
@login_required
def post_questionnaire(eq_id, form_type, period_id, collection_id, location):
    logger.debug("Post location : /questionnaire/%s/%s/%s/%s/%s", eq_id, form_type, period_id, collection_id, location)
    questionnaire_manager = QuestionnaireManagerFactory.get_instance()
    if not same_survey(collection_id, eq_id, form_type, period_id):
        return redirect("/information/multiple-surveys")
    elif questionnaire_manager.submitted:
        return do_redirect(eq_id, form_type, period_id, collection_id, 'thank-you')

    try:
        logger.debug("POST current location %s", location)
        logger.debug("POST request length %s", request.content_length)

        questionnaire_manager.process_incoming_answers(location, request.form)
        next_location = questionnaire_manager.get_current_location()
        metadata = get_metadata(current_user)
        logger.info("Redirecting user to next location %s with tx_id=%s", next_location, metadata.tx_id)
        return do_redirect(eq_id, form_type, period_id, collection_id, next_location)
    except InvalidLocationException:
        return do_redirect(eq_id, form_type, period_id, collection_id, questionnaire_manager.get_current_location())


@main_blueprint.route('/questionnaire/<eq_id>/<form_type>/<period_id>/<collection_id>/previous', methods=['GET'])
@login_required
def go_to_previous_page(eq_id, form_type, period_id, collection_id):
    questionnaire_manager = QuestionnaireManagerFactory.get_instance()
    if not same_survey(collection_id, eq_id, form_type, period_id):
        return redirect("/information/multiple-surveys")
    elif questionnaire_manager.submitted:
        return do_redirect(eq_id, form_type, period_id, collection_id, 'thank-you')

    previous_location = questionnaire_manager.get_previous_location()
    questionnaire_manager.go_to(previous_location)
    return do_redirect(eq_id, form_type, period_id, collection_id, previous_location)


@main_blueprint.route('/questionnaire/<eq_id>/<form_type>/<period_id>/<collection_id>/thank-you', methods=["GET"])
@login_required
def get_thank_you(eq_id, form_type, period_id, collection_id):
    # Delete user data on request of thank you page.
    questionnaire_manager = QuestionnaireManagerFactory.get_instance()
    if not same_survey(collection_id, eq_id, form_type, period_id):
        return redirect("/information/multiple-surveys")

    page = render_page('thank-you', questionnaire_manager)
    questionnaire_manager.delete_user_data()
    return page


def do_redirect(eq_id, form_type, period_id, collection_id,  location):
    return redirect('/questionnaire/' + eq_id + '/' + form_type + '/' + period_id + '/' + collection_id + '/' + location)


def same_survey(collection_id, eq_id, form_type, period_id):
    metadata = get_metadata(current_user)
    current_survey = eq_id + form_type + period_id + collection_id
    metadata_survey = metadata.eq_id + metadata.form_type + metadata.period_id + metadata.collection_exercise_sid
    return current_survey == metadata_survey


def render_page(location, questionnaire_manager):
    questionnaire_manager.go_to(location)
    context = questionnaire_manager.get_rendering_context(location)
    template = questionnaire_manager.get_rendering_template(location)
    try:
        theme = context['meta']['survey']['theme']
        logger.debug("Theme selected: {} ".format(theme))
    except KeyError:
        logger.info("No theme set ")
        theme = None
    return render_theme_template(theme, template, meta=context['meta'], content=context['content'])

import logging

from functools import wraps

from app.authentication.session_management import session_manager
from app.data_model.questionnaire_store import get_metadata, get_questionnaire_store
from app.questionnaire.questionnaire_manager import InvalidLocationException
from app.questionnaire.questionnaire_manager_factory import QuestionnaireManagerFactory
from app.templating.template_register import TemplateRegistry

from flask import redirect
from flask import request
from flask import Blueprint

from flask_login import current_user
from flask_login import login_required

from flask_themes2 import render_theme_template

logger = logging.getLogger(__name__)


questionnaire_blueprint = Blueprint(name='questionnaire',
                                    import_name=__name__,
                                    url_prefix='/questionnaire/<eq_id>/<form_type>/<period_id>/<collection_id>/')


def check_survey_state(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        questionnaire_manager = QuestionnaireManagerFactory.get_instance()
        survey_submitted = questionnaire_manager.submitted_at is not None
        if survey_submitted:
            return do_redirect(kwargs['eq_id'], kwargs['form_type'], kwargs['period_id'], kwargs['collection_id'], 'thank-you')
        elif not same_survey(kwargs['eq_id'], kwargs['form_type'], kwargs['period_id'], kwargs['collection_id']):
            return redirect("/information/multiple-surveys")
        else:
            return func(*args, **kwargs)

    return decorated_function


@questionnaire_blueprint.after_request
def add_cache_control(response):
    response.cache_control.no_cache = True
    return response


@questionnaire_blueprint.route('<location>', methods=["GET"])
@login_required
@check_survey_state
def get_questionnaire(eq_id, form_type, period_id, collection_id, location):
    return get_page(collection_id, eq_id, form_type, period_id, location)


@questionnaire_blueprint.route('<location>', methods=["POST"])
@login_required
@check_survey_state
def post_questionnaire(eq_id, form_type, period_id, collection_id, location):
    questionnaire_manager = QuestionnaireManagerFactory.get_instance()
    try:
        questionnaire_manager.process_incoming_answers(location, request.form)
    except InvalidLocationException:
        return do_redirect(eq_id, form_type, period_id, collection_id, questionnaire_manager.get_current_location())

    next_location = questionnaire_manager.get_current_location()
    metadata = get_metadata(current_user)
    logger.info("Redirecting user to next location %s with tx_id=%s", next_location, metadata["tx_id"])
    return do_redirect(eq_id, form_type, period_id, collection_id, next_location)


@questionnaire_blueprint.route('previous', methods=['GET'])
@login_required
@check_survey_state
def go_to_previous_page(eq_id, form_type, period_id, collection_id):
    questionnaire_manager = QuestionnaireManagerFactory.get_instance()
    previous_location = questionnaire_manager.get_previous_location()
    try:
        questionnaire_manager.go_to(previous_location)
    except InvalidLocationException:
        return do_redirect(eq_id, form_type, period_id, collection_id, questionnaire_manager.get_current_location())
    return do_redirect(eq_id, form_type, period_id, collection_id, previous_location)


@questionnaire_blueprint.route('thank-you', methods=["GET"])
@login_required
def get_thank_you(eq_id, form_type, period_id, collection_id):
    if not same_survey(eq_id, form_type, period_id, collection_id):
        return redirect("/information/multiple-surveys")

    page = get_page(collection_id, eq_id, form_type, period_id, 'thank-you')
    # Delete user data on request of thank you page.
    delete_user_data()
    return page


@questionnaire_blueprint.route('summary', methods=["GET"])
@login_required
@check_survey_state
def get_summary(eq_id, form_type, period_id, collection_id):
    return get_page(collection_id, eq_id, form_type, period_id, 'summary')


def delete_user_data():
    get_questionnaire_store(current_user.user_id, current_user.user_ik).delete()
    session_manager.clear()


def do_redirect(eq_id, form_type, period_id, collection_id,  location):
    return redirect('/questionnaire/' + eq_id + '/' + form_type + '/' + period_id + '/' + collection_id + '/' + location)


def same_survey(eq_id, form_type, period_id, collection_id):
    metadata = get_metadata(current_user)
    current_survey = eq_id + form_type + period_id + collection_id
    metadata_survey = metadata["eq_id"] + metadata["form_type"] + metadata["period_id"] + metadata["collection_exercise_sid"]
    return current_survey == metadata_survey


def get_page(collection_id, eq_id, form_type, period_id, location):
    questionnaire_manager = QuestionnaireManagerFactory.get_instance()
    try:
        questionnaire_manager.go_to(location)
    except InvalidLocationException:
        return do_redirect(eq_id, form_type, period_id, collection_id, questionnaire_manager.get_current_location())
    context = questionnaire_manager.get_rendering_context(location)
    template = get_rendering_template(location)
    return render_template(template, context)


def render_template(template, context):
    try:
        theme = context['meta']['survey']['theme']
        logger.debug("Theme selected: {} ".format(theme))
    except KeyError:
        logger.info("No theme set ")
        theme = None
    return render_theme_template(theme, template, meta=context['meta'], content=context['content'])


def get_rendering_template(location):
    return TemplateRegistry.get_template_name(location)

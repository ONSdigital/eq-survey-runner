import logging

from app.authentication.session_management import session_manager
from app.globals import get_answers, get_completed_blocks, get_metadata, get_questionnaire_store
from app.questionnaire.questionnaire_manager import QuestionnaireManager
from app.submitter.submitter import SubmitterFactory
from app.templating.template_register import TemplateRegistry
from app.utilities.schema import get_schema

from flask import redirect
from flask import request
from flask import Blueprint
from flask import g
from flask import url_for

from flask_login import current_user
from flask_login import login_required

from flask_themes2 import render_theme_template


logger = logging.getLogger(__name__)


questionnaire_blueprint = Blueprint(name='questionnaire',
                                    import_name=__name__,
                                    url_prefix='/questionnaire/<eq_id>/<form_type>/<collection_id>/')


@questionnaire_blueprint.before_request
@login_required
def check_survey_state():
    json, schema = get_schema()
    g.questionnaire_manager = QuestionnaireManager(schema, json=json)
    values = request.view_args

    if not same_survey(values['eq_id'], values['form_type'], values['collection_id']):
        return redirect(url_for('root.information', message_identifier='multiple-surveys'))


@questionnaire_blueprint.after_request
def add_cache_control(response):
    response.cache_control.no_cache = True
    return response


@questionnaire_blueprint.route('<block_id>', methods=["GET"])
@login_required
def get_block(eq_id, form_type, collection_id, block_id):
    context = g.questionnaire_manager.get_rendering_context(block_id, True)
    template = TemplateRegistry.get_template_name(block_id)
    navigator = g.questionnaire_manager.navigator
    answers = get_answers(current_user)
    previous_location = navigator.get_previous_location(answers, block_id)

    return render_template(template, context, previous_location)


@questionnaire_blueprint.route('<block_id>/<iteration>', methods=["GET"])
@login_required
def get_block_iteration(eq_id, form_type, collection_id, block_id, iteration):
    context = g.questionnaire_manager.get_rendering_context(block_id, True)
    template = TemplateRegistry.get_template_name(block_id)
    navigator = g.questionnaire_manager.navigator
    answers = get_answers(current_user)

    previous_location = navigator.get_previous_location(answers, block_id, int(iteration))

    return render_template(template, context, previous_location)


@questionnaire_blueprint.route('<block_id>', defaults={'iteration': 0}, methods=["POST"])
@questionnaire_blueprint.route('<block_id>/<iteration>', methods=["POST"])
@login_required
def post_block_iteration(eq_id, form_type, collection_id, block_id, iteration):
    valid = g.questionnaire_manager.process_incoming_answers(block_id, request.form)

    if not valid:
        return render_page(block_id, False)

    iteration = int(iteration)
    completed_blocks = get_completed_blocks(current_user)

    logger.info("Location %s", block_id)
    logger.info("Visited blocks %s", str(completed_blocks))
    logger.info("current_iteration is %d", iteration)

    navigator = g.questionnaire_manager.navigator
    answers = get_answers(current_user)
    next_block_id = navigator.get_next_location(answers, block_id, iteration)

    logger.info("Next block appears %d times in history", completed_blocks.count(next_block_id))
    logger.info("Next block appears %d times in path", navigator.block_in_path_count(answers, next_block_id))

    next_iteration = 0

    if completed_blocks.count(next_block_id) > 0 and navigator.block_in_path_count(answers, next_block_id) > 1:
        next_iteration = completed_blocks.count(next_block_id)

    logger.info("Next iteration is %d", next_iteration)

    metadata = get_metadata(current_user)

    logger.info("Redirecting user to next location %s with tx_id=%s", next_block_id, metadata["tx_id"])

    return redirect_to_block(eq_id, form_type, collection_id, next_block_id)


@questionnaire_blueprint.route('summary', methods=["GET"])
@login_required
def get_summary(eq_id, form_type, collection_id):
    navigator = g.questionnaire_manager.navigator
    latest_location = navigator.get_latest_location(get_answers(current_user), get_completed_blocks(current_user))
    if latest_location is 'summary':
        return render_page('summary', True)
    return redirect_to_block(eq_id, form_type, collection_id, latest_location)


@questionnaire_blueprint.route('thank-you', methods=["GET"])
@login_required
def get_thank_you(eq_id, form_type, collection_id):
    if not same_survey(eq_id, form_type, collection_id):
        return redirect("/information/multiple-surveys")

    thank_you_page = render_page('thank-you', True)
    # Delete user data on request of thank you page.
    delete_user_data()
    return thank_you_page


@questionnaire_blueprint.route('submit-answers', methods=["POST"])
@login_required
def submit_answers(eq_id, form_type, collection_id):
    answers = get_answers(current_user)

    # check that all the answers we have are valid before submitting the data
    is_valid, invalid_location = g.questionnaire_manager.validate_all_answers()

    if is_valid:
        submitter = SubmitterFactory.get_submitter()
        submitter.send_answers(get_metadata(current_user), g.questionnaire_manager.get_schema(), answers)

        return redirect_to_block(eq_id, form_type, collection_id, 'thank-you')
    else:
        return redirect_to_block(eq_id, form_type, collection_id, invalid_location)


def delete_user_data():
    get_questionnaire_store(current_user.user_id, current_user.user_ik).delete()
    session_manager.clear()


def redirect_to_block(eq_id, form_type, collection_id, block_id, iteration=0):
    kwargs = {
        "eq_id": eq_id,
        "form_type": form_type,
        "collection_id": collection_id,
        "block_id": block_id,
    }
    if iteration == 0:
        return redirect(url_for('.get_block', **kwargs))

    kwargs['iteration'] = iteration

    return redirect(url_for('.get_block_iteration', **kwargs))


def same_survey(eq_id, form_type, collection_id):
    metadata = get_metadata(current_user)
    current_survey = eq_id + form_type + collection_id
    metadata_survey = metadata["eq_id"] + metadata["form_type"] + metadata["collection_exercise_sid"]
    return current_survey == metadata_survey


def render_page(location, is_valid):
    context = g.questionnaire_manager.get_rendering_context(location, is_valid)
    template = TemplateRegistry.get_template_name(location)
    navigator = g.questionnaire_manager.navigator
    previous_location = navigator.get_previous_location(get_answers(current_user), location)
    return render_template(template, context, previous_location)


def render_template(template, context, previous_location):
    try:
        theme = context['meta']['survey']['theme']
        logger.debug("Theme selected: {} ".format(theme))
    except KeyError:
        logger.info("No theme set ")
        theme = None
    return render_theme_template(theme, template, meta=context['meta'], content=context['content'], previous_location=previous_location)

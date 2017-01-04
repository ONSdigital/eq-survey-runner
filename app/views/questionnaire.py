import logging

from app.authentication.session_manager import session_manager
from app.globals import get_answer_store, get_completed_blocks, get_metadata, get_questionnaire_store
from app.helpers.schema_helper import SchemaHelper
from app.questionnaire.location import Location
from app.questionnaire.navigator import Navigator
from app.questionnaire.questionnaire_manager import get_questionnaire_manager
from app.submitter.converter import convert_answers
from app.submitter.submitter import SubmitterFactory
from app.templating.introduction_context import get_introduction_context
from app.templating.metadata_context import build_metadata_context
from app.templating.schema_context import build_schema_context
from app.templating.summary_context import build_summary_rendering_context
from app.templating.template_renderer import renderer
from app.utilities.schema import get_schema
from app.views.errors import MultipleSurveyError

from flask import redirect
from flask import request
from flask import Blueprint
from flask import g
from flask import url_for

from flask_login import current_user
from flask_login import login_required

from flask_themes2 import render_theme_template

from werkzeug.exceptions import NotFound

logger = logging.getLogger(__name__)


questionnaire_blueprint = Blueprint(name='questionnaire',
                                    import_name=__name__,
                                    url_prefix='/questionnaire/<form_type>/<collection_id>/')


@questionnaire_blueprint.before_request
@login_required
def check_survey_state():
    metadata = get_metadata(current_user)
    g.schema_json, g.schema = get_schema(metadata)
    values = request.view_args

    _check_same_survey(metadata, values['form_type'], values['collection_id'])


@questionnaire_blueprint.after_request
def add_cache_control(response):
    response.cache_control.no_cache = True

    return response


@questionnaire_blueprint.after_request
def save_questionnaire_store(response):
    if not current_user.is_anonymous:
        questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)

        if questionnaire_store.has_changed():
            questionnaire_store.save()

    return response


@questionnaire_blueprint.route('<group_id>/<int:group_instance>/<block_id>', methods=["GET"])
@login_required
def get_block(form_type, collection_id, group_id, group_instance, block_id):
    # Filter answers down to those we may need to render
    answer_store = get_answer_store(current_user)
    answers = answer_store.map(group_id=group_id, group_instance=group_instance, block_id=block_id)

    this_location = Location(group_id, group_instance, block_id)

    q_manager = get_questionnaire_manager(g.schema, g.schema_json)
    q_manager.build_state(this_location, answers)

    block = g.schema.get_item_by_id(block_id)
    template = block.type if block and block.type else 'questionnaire'

    current_location = Location(group_id, group_instance, block_id)

    return _render_template(q_manager.state, current_location=current_location, template=template)


@questionnaire_blueprint.route('<group_id>/<int:group_instance>/<block_id>', methods=["POST"])
@login_required
def post_block(form_type, collection_id, group_id, group_instance, block_id):
    navigator = Navigator(g.schema_json, get_metadata(current_user), get_answer_store(current_user))
    q_manager = get_questionnaire_manager(g.schema, g.schema_json)

    this_location = Location(group_id, group_instance, block_id)

    valid_location = this_location in navigator.get_routing_path(group_id, group_instance)
    valid_data = q_manager.validate(this_location, request.form)

    if not valid_location or not valid_data:
        return _render_template(q_manager.state, block_id=block_id, template='questionnaire')
    else:
        q_manager.update_questionnaire_store(this_location)

    next_location = navigator.get_next_location(current_location=this_location)
    metadata = get_metadata(current_user)

    if next_location is None:
        raise NotFound

    if next_location.block_id == 'confirmation':
        return redirect_to_confirmation(form_type, collection_id)

    return redirect(next_location.url(metadata))


@questionnaire_blueprint.route('introduction', methods=["GET"])
@login_required
def get_introduction(form_type, collection_id):
    return _render_template(get_introduction_context(g.schema_json), block_id='introduction')


@questionnaire_blueprint.route('<block_id>', methods=["POST"])
@login_required
def post_interstitial(form_type, collection_id, block_id):
    navigator = Navigator(g.schema_json, get_metadata(current_user), get_answer_store(current_user))
    q_manager = get_questionnaire_manager(g.schema, g.schema_json)

    this_location = Location(SchemaHelper.get_first_group_id(g.schema_json), 0, block_id)

    valid_location = this_location in navigator.get_location_path()
    q_manager.process_incoming_answers(this_location, request.form)

    # Don't care if data is valid because there isn't any for interstitial
    if not valid_location:
        return _render_template(q_manager.state, current_location=this_location, template='questionnaire')

    next_location = navigator.get_next_location(current_location=this_location)
    metadata = get_metadata(current_user)

    if next_location is None:
        raise NotFound

    logger.info("Redirecting user to next location %s with tx_id=%s", str(next_location), metadata["tx_id"])

    return redirect(next_location.url(metadata))


@questionnaire_blueprint.route('summary', methods=["GET"])
@login_required
def get_summary(form_type, collection_id):

    answer_store = get_answer_store(current_user)
    navigator = Navigator(g.schema_json, get_metadata(current_user), answer_store)
    latest_location = navigator.get_latest_location(get_completed_blocks(current_user))
    metadata = get_metadata(current_user)

    if latest_location.block_id is 'summary':
        answers = get_answer_store(current_user)
        schema_context = build_schema_context(metadata, g.schema.aliases, answers)
        rendered_schema_json = renderer.render(g.schema_json, **schema_context)
        summary_context = build_summary_rendering_context(rendered_schema_json, answer_store, metadata)
        return _render_template(summary_context, current_location=latest_location)

    return redirect(latest_location.url(metadata))


@questionnaire_blueprint.route('confirmation', methods=["GET"])
@login_required
def get_confirmation(form_type, collection_id):
    answer_store = get_answer_store(current_user)
    navigator = Navigator(g.schema_json, get_metadata(current_user), answer_store)

    latest_location = navigator.get_latest_location(get_completed_blocks(current_user))

    if latest_location.block_id == 'confirmation':

        q_manager = get_questionnaire_manager(g.schema, g.schema_json)
        this_location = Location(SchemaHelper.get_first_group_id(g.schema_json), 0, 'confirmation')
        q_manager.build_state(this_location, answer_store)

        return _render_template(q_manager.state, current_location=latest_location)

    metadata = get_metadata(current_user)

    return redirect(latest_location.url(metadata))


@questionnaire_blueprint.route('thank-you', methods=["GET"])
@login_required
def get_thank_you(form_type, collection_id):
    thank_you_page = _render_template(get_questionnaire_manager(g.schema, g.schema_json).state, block_id='thank-you')
    # Delete user data on request of thank you page.
    _delete_user_data()
    return thank_you_page


@questionnaire_blueprint.route('submit-answers', methods=["POST"])
@login_required
def submit_answers(form_type, collection_id):
    q_manager = get_questionnaire_manager(g.schema, g.schema_json)
    # check that all the answers we have are valid before submitting the data
    is_valid, invalid_location = q_manager.validate_all_answers()
    metadata = get_metadata(current_user)

    if is_valid:
        answer_store = get_answer_store(current_user)
        navigator = Navigator(g.schema_json, metadata, answer_store)
        submitter = SubmitterFactory.get_submitter()
        message = convert_answers(metadata, g.schema, answer_store, navigator.get_routing_path())
        submitter.send_answers(message)
        logger.info("Responses submitted tx_id=%s", metadata["tx_id"])
        return redirect_to_thank_you(form_type, collection_id)
    else:
        return redirect(invalid_location.url(metadata))


@questionnaire_blueprint.route('<group_id>/0/household-composition', methods=["POST"])
@login_required
def post_household_composition(form_type, collection_id, group_id):
    navigator = Navigator(g.schema_json, get_metadata(current_user), get_answer_store(current_user))
    questionnaire_manager = get_questionnaire_manager(g.schema, g.schema_json)
    answer_store = get_answer_store(current_user)

    this_location = Location(group_id, 0, 'household-composition')

    if 'action[save_continue]' in request.form:
        _remove_repeating_on_household_answers(answer_store, group_id)

    valid = questionnaire_manager.process_incoming_answers(this_location, request.form)

    if 'action[add_answer]' in request.form:
        questionnaire_manager.add_answer(this_location, 'household-composition-question', answer_store)
        return get_block(form_type, collection_id, group_id, 0, 'household-composition')

    elif 'action[remove_answer]' in request.form:
        index_to_remove = int(request.form.get('action[remove_answer]'))
        questionnaire_manager.remove_answer(this_location, answer_store, index_to_remove)
        return get_block(form_type, collection_id, group_id, 0, 'household-composition')

    if not valid:
        return _render_template(questionnaire_manager.state, current_location=this_location, template='questionnaire')

    next_location = navigator.get_next_location(current_location=this_location)

    metadata = get_metadata(current_user)

    return redirect(next_location.url(metadata))


@questionnaire_blueprint.route('<group_id>/<int:group_instance>/permanent-or-family-home', methods=["POST"])
@login_required
def post_everyone_at_address_confirmation(form_type, collection_id, group_id, group_instance):
    if request.form.get('permanent-or-family-home-answer') == 'No':
        _remove_repeating_on_household_answers(get_answer_store(current_user), group_id)
    return post_block(form_type, collection_id, group_id, group_instance, 'permanent-or-family-home')


def _remove_repeating_on_household_answers(answer_store, group_id):
    answer_store.remove(group_id=group_id, block_id='household-composition')
    questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)
    for answer in SchemaHelper.get_answers_that_repeat_in_block(g.schema_json, 'household-composition'):
        groups_to_delete = SchemaHelper.get_groups_that_repeat_with_answer_id(g.schema_json, answer['id'])
        for group in groups_to_delete:
            answer_store.remove(group_id=group['id'])
            questionnaire_store.completed_blocks[:] = [b for b in questionnaire_store.completed_blocks if
                                                       b.group_id != group['id']]


def _delete_user_data():
    get_questionnaire_store(current_user.user_id, current_user.user_ik).delete()
    session_manager.clear()


def redirect_to_thank_you(form_type, collection_id):
    return redirect(interstitial_url(form_type, collection_id, 'thank-you'))


def redirect_to_confirmation(form_type, collection_id):
    return redirect(interstitial_url(form_type, collection_id, 'confirmation'))


def interstitial_url(form_type, collection_id, block_id):
    if block_id == 'summary':
        return url_for('.get_summary',
                       form_type=form_type,
                       collection_id=collection_id)
    elif block_id == 'introduction':
        return url_for('.get_introduction',
                       form_type=form_type,
                       collection_id=collection_id)
    elif block_id == 'confirmation':
        return url_for('.get_confirmation',
                       form_type=form_type,
                       collection_id=collection_id)
    elif block_id == 'thank-you':
        return url_for('.get_thank_you',
                       form_type=form_type,
                       collection_id=collection_id)


def _check_same_survey(metadata, form_type, collection_id):
    if form_type != metadata["form_type"] or collection_id != metadata["collection_exercise_sid"]:
        raise MultipleSurveyError


def _render_template(context, current_location=None, block_id=None, template=None):
    metadata = get_metadata(current_user)
    metadata_context = build_metadata_context(metadata)

    if current_location is None:
        group_id = SchemaHelper.get_first_group_id(g.schema_json)
        current_location = Location(group_id, 0, block_id)

    navigator = Navigator(g.schema_json, get_metadata(current_user), get_answer_store(current_user))
    completed_blocks = get_completed_blocks(current_user)
    front_end_navigation = navigator.get_front_end_navigation(
        completed_blocks,
        current_location.group_id,
        current_location.group_instance,
    )
    previous_location = navigator.get_previous_location(current_location)

    previous_url = None

    if previous_location is not None and current_location.block_id != SchemaHelper.get_first_block_id_for_group(g.schema_json, current_location.group_id):
        previous_url = previous_location.url(metadata)

    try:
        theme = g.schema_json['theme']
        logger.debug("Theme selected: %s", theme)
    except KeyError:
        logger.info("No theme set")
        theme = None

    template = '{}.html'.format(template or current_location.block_id)

    return render_theme_template(theme, template, meta=metadata_context,
                                 content=context,
                                 previous_location=previous_url,
                                 navigation=front_end_navigation,
                                 schema_title=g.schema_json['title'])

from flask import Blueprint
from flask import g
from flask import redirect
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_themes2 import render_theme_template
from structlog import get_logger
from werkzeug.exceptions import NotFound

from app.authentication.session_storage import session_storage
from app.globals import get_answer_store, get_completed_blocks, get_metadata, get_questionnaire_store
from app.helpers.schema_helper import SchemaHelper
from app.questionnaire.location import Location
from app.questionnaire.navigation import Navigation
from app.questionnaire.path_finder import PathFinder
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

logger = get_logger()


questionnaire_blueprint = Blueprint(name='questionnaire',
                                    import_name=__name__,
                                    url_prefix='/questionnaire/<eq_id>/<form_type>/<collection_id>/')


@questionnaire_blueprint.before_request
@login_required
def check_survey_state():
    metadata = get_metadata(current_user)
    logger.new(tx_id=metadata['tx_id'])
    values = request.view_args
    logger.debug('questionnaire request', eq_id=values['eq_id'], form_type=values['form_type'],
                 ce_id=values['collection_id'], method=request.method, url_path=request.full_path)
    g.schema_json, g.schema = get_schema(metadata)
    _check_same_survey(values['eq_id'], values['form_type'], values['collection_id'])


@questionnaire_blueprint.after_request
def add_cache_control(response):
    response.cache_control.no_cache = True

    return response


@questionnaire_blueprint.after_request
def save_questionnaire_store(response):
    if not current_user.is_anonymous:
        questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)

        if questionnaire_store.has_changed():
            questionnaire_store.add_or_update()

    return response


@questionnaire_blueprint.route('<group_id>/<int:group_instance>/<block_id>', methods=["GET"])
@login_required
def get_block(eq_id, form_type, collection_id, group_id, group_instance, block_id):  # pylint: disable=unused-argument
    # Filter answers down to those we may need to render
    answer_store = get_answer_store(current_user)
    answers = answer_store.map(group_id=group_id, group_instance=group_instance, block_id=block_id)

    this_location = Location(group_id, group_instance, block_id)

    q_manager = get_questionnaire_manager(g.schema, g.schema_json)
    q_manager.build_block_state(this_location, answers)

    # Find block by id
    block = g.schema.get_item_by_id(block_id)
    # pylint: disable=maybe-no-member
    template = block.type if block and block.type else 'questionnaire'

    current_location = Location(group_id, group_instance, block_id)

    _render_schema(current_location)
    return _build_template(current_location, q_manager.block_state, template)


@questionnaire_blueprint.route('<group_id>/<int:group_instance>/<block_id>', methods=["POST"])
@login_required
def post_block(eq_id, form_type, collection_id, group_id, group_instance, block_id):
    path_finder = PathFinder(g.schema_json, get_answer_store(current_user), get_metadata(current_user))
    q_manager = get_questionnaire_manager(g.schema, g.schema_json)

    this_location = Location(group_id, group_instance, block_id)
    if 'action[save_sign_out]' in request.form:
        return _save_sign_out(collection_id, eq_id, form_type, q_manager, this_location)

    valid_location = this_location in path_finder.get_routing_path(group_id, group_instance)
    valid_data = q_manager.validate(this_location, request.form)

    if not valid_location or not valid_data:
        current_location = Location(group_id, group_instance, block_id)
        _render_schema(current_location)
        return _build_template(current_location, q_manager.block_state, template='questionnaire')
    else:
        q_manager.update_questionnaire_store(this_location)

    next_location = path_finder.get_next_location(current_location=this_location)

    if next_location is None:
        raise NotFound

    metadata = get_metadata(current_user)
    return redirect(next_location.url(metadata))


@questionnaire_blueprint.route('introduction', methods=["GET"])
@login_required
def get_introduction(eq_id, form_type, collection_id):  # pylint: disable=unused-argument
    group_id = SchemaHelper.get_first_group_id(g.schema_json)
    current_location = Location(group_id, group_instance=0, block_id='introduction')
    return _build_template(current_location, get_introduction_context(g.schema_json))


@questionnaire_blueprint.route('<block_id>', methods=["POST"])
@login_required
def post_interstitial(eq_id, form_type, collection_id, block_id):  # pylint: disable=unused-argument
    path_finder = PathFinder(g.schema_json, get_answer_store(current_user), get_metadata(current_user))
    q_manager = get_questionnaire_manager(g.schema, g.schema_json)

    this_location = Location(SchemaHelper.get_first_group_id(g.schema_json), group_instance=0, block_id=block_id)

    q_manager.update_questionnaire_store(this_location)

    # Don't care if data is valid because there isn't any for interstitial
    if this_location not in path_finder.get_location_path():
        _render_schema(this_location)
        return _build_template(current_location=this_location, context=q_manager.block_state, template='questionnaire')

    next_location = path_finder.get_next_location(current_location=this_location)

    if next_location is None:
        raise NotFound

    metadata = get_metadata(current_user)
    next_location_url = next_location.url(metadata)
    logger.debug("redirecting", url=next_location_url)
    return redirect(next_location_url)


@questionnaire_blueprint.route('summary', methods=["GET"])
@login_required
def get_summary(eq_id, form_type, collection_id):  # pylint: disable=unused-argument
    answer_store = get_answer_store(current_user)
    path_finder = PathFinder(g.schema_json, answer_store, get_metadata(current_user))
    latest_location = path_finder.get_latest_location(get_completed_blocks(current_user))
    metadata = get_metadata(current_user)

    if latest_location.block_id is 'summary':
        answers = get_answer_store(current_user)
        schema_context = build_schema_context(metadata, g.schema.aliases, answers)
        rendered_schema_json = renderer.render(g.schema_json, **schema_context)
        summary_context = build_summary_rendering_context(rendered_schema_json, answer_store, metadata)
        return _build_template(current_location=latest_location, context=summary_context)

    return redirect(latest_location.url(metadata))


@questionnaire_blueprint.route('confirmation', methods=["GET"])
@login_required
def get_confirmation(eq_id, form_type, collection_id):  # pylint: disable=unused-argument
    answer_store = get_answer_store(current_user)
    path_finder = PathFinder(g.schema_json, answer_store, get_metadata(current_user))

    latest_location = path_finder.get_latest_location(get_completed_blocks(current_user))

    if latest_location.block_id == 'confirmation':
        q_manager = get_questionnaire_manager(g.schema, g.schema_json)
        q_manager.build_block_state(latest_location, answer_store)

        _render_schema(latest_location)
        return _build_template(current_location=latest_location, context=q_manager.block_state)

    metadata = get_metadata(current_user)

    return redirect(latest_location.url(metadata))


@questionnaire_blueprint.route('thank-you', methods=["GET"])
@login_required
def get_thank_you(eq_id, form_type, collection_id):  # pylint: disable=unused-argument
    group_id = SchemaHelper.get_last_group_id(g.schema_json)
    current_location = Location(group_id, group_instance=0, block_id='thank-you')
    thank_you_page = _build_template(current_location=current_location)
    # Delete user data on request of thank you page.
    _delete_user_data()
    return thank_you_page


@questionnaire_blueprint.route('signed-out', methods=["GET"])
@login_required
def get_sign_out(eq_id, form_type, collection_id):  # pylint: disable=unused-argument
    signed_out_page = _render_template(get_questionnaire_manager(g.schema, g.schema_json), block_id='signed-out')
    session_storage.clear()
    return signed_out_page


@questionnaire_blueprint.route('submit-answers', methods=["POST"])
@login_required
def submit_answers(eq_id, form_type, collection_id):
    q_manager = get_questionnaire_manager(g.schema, g.schema_json)
    # check that all the answers we have are valid before submitting the data
    is_valid, invalid_location = q_manager.validate_all_answers()
    metadata = get_metadata(current_user)

    if is_valid:
        answer_store = get_answer_store(current_user)
        path_finder = PathFinder(g.schema_json, answer_store, metadata)
        submitter = SubmitterFactory.get_submitter()
        message = convert_answers(metadata, g.schema, answer_store, path_finder.get_routing_path())
        submitter.send_answers(message)
        return redirect(url_for('.get_thank_you', eq_id=eq_id, form_type=form_type, collection_id=collection_id))
    else:
        return redirect(invalid_location.url(metadata))


@questionnaire_blueprint.route('<group_id>/0/household-composition', methods=["POST"])
@login_required
def post_household_composition(eq_id, form_type, collection_id, group_id):
    questionnaire_manager = get_questionnaire_manager(g.schema, g.schema_json)
    answer_store = get_answer_store(current_user)

    this_location = Location(group_id, group_instance=0, block_id='household-composition')

    if 'action[save_continue]' in request.form:
        _remove_repeating_on_household_answers(answer_store, group_id)

    valid = questionnaire_manager.process_incoming_answers(this_location, post_data=request.form)

    if 'action[add_answer]' in request.form:
        questionnaire_manager.add_answer(this_location, answer_store, question_id='household-composition-question')
        return get_block(eq_id, form_type, collection_id, group_id, group_instance=0, block_id='household-composition')

    elif 'action[remove_answer]' in request.form:
        index_to_remove = int(request.form.get('action[remove_answer]'))
        questionnaire_manager.remove_answer(this_location, answer_store, index_to_remove)
        return get_block(eq_id, form_type, collection_id, group_id, group_instance=0, block_id='household-composition')

    elif 'action[save_sign_out]' in request.form:
        return _save_sign_out(collection_id, eq_id, form_type, questionnaire_manager, this_location)

    if not valid:
        _render_schema(this_location)
        return _build_template(current_location=this_location, context=questionnaire_manager.block_state,
                               template='questionnaire')

    path_finder = PathFinder(g.schema_json, get_answer_store(current_user), get_metadata(current_user))
    next_location = path_finder.get_next_location(current_location=this_location)

    metadata = get_metadata(current_user)

    return redirect(next_location.url(metadata))


@questionnaire_blueprint.route('<group_id>/<int:group_instance>/permanent-or-family-home', methods=["POST"])
@login_required
def post_everyone_at_address_confirmation(eq_id, form_type, collection_id, group_id, group_instance):
    if request.form.get('permanent-or-family-home-answer') == 'No':
        _remove_repeating_on_household_answers(get_answer_store(current_user), group_id)
    return post_block(eq_id, form_type, collection_id, group_id, group_instance, 'permanent-or-family-home')


def _save_sign_out(collection_id, eq_id, form_type, q_manager, this_location):
    valid_data = q_manager.validate(this_location, request.form, skip_mandatory_validation=True)
    if not valid_data:
        return _build_template(this_location, q_manager.block_state, template='questionnaire')
    else:
        q_manager.update_questionnaire_store_save_sign_out(this_location)
        return redirect(url_for('.get_sign_out', eq_id=eq_id, form_type=form_type, collection_id=collection_id))


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
    session_storage.clear()


def _check_same_survey(eq_id, form_type, collection_id):
    metadata = get_metadata(current_user)
    current_survey = eq_id + form_type + collection_id
    metadata_survey = metadata["eq_id"] + metadata["form_type"] + metadata["collection_exercise_sid"]
    if current_survey != metadata_survey:
        raise MultipleSurveyError


def _render_schema(current_location):
    metadata = get_metadata(current_user)
    answer_store = get_answer_store(current_user)
    schema_item = g.schema.get_item_by_id(current_location.block_id)
    schema_context = build_schema_context(metadata, g.schema.aliases, answer_store, current_location.group_instance)
    renderer.render_schema_items(schema_item, schema_context)


def _build_template(current_location, context=None, template=None):
    metadata = get_metadata(current_user)
    metadata_context = build_metadata_context(metadata)

    answer_store = get_answer_store(current_user)
    completed_blocks = get_completed_blocks(current_user)

    navigation = Navigation(g.schema_json, answer_store, metadata, completed_blocks)
    front_end_navigation = navigation.build_navigation(current_location.group_id, current_location.group_instance)

    path_finder = PathFinder(g.schema_json, answer_store, metadata)
    previous_location = path_finder.get_previous_location(current_location)

    previous_url = None

    is_first_block_for_group = SchemaHelper.is_first_block_id_for_group(g.schema_json, current_location.group_id, current_location.block_id)

    if previous_location is not None and not is_first_block_for_group and not current_location.block_id == 'thank-you':
        previous_url = previous_location.url(metadata)

    return _render_template(context, current_location.block_id, front_end_navigation, metadata_context, previous_url, template)


def _render_template(context, block_id, front_end_navigation=None, metadata_context=None, previous_url=None, template=None):
    theme = g.schema_json.get('theme', None)
    logger.debug("theme selected", theme=theme)
    template = '{}.html'.format(template or block_id)
    return render_theme_template(theme, template, meta=metadata_context,
                                 content=context,
                                 previous_location=previous_url,
                                 navigation=front_end_navigation,
                                 schema_title=g.schema_json['title'],
                                 legal_basis=g.schema_json['legal_basis'],
                                 survey_id=g.schema_json['survey_id'],
                                 )

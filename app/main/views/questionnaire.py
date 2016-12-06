import logging

from app.authentication.session_manager import session_manager
from app.globals import get_answer_store, get_completed_blocks, get_metadata, get_questionnaire_store
from app.helpers.schema_helper import SchemaHelper
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
                                    url_prefix='/questionnaire/<eq_id>/<form_type>/<collection_id>/')


@questionnaire_blueprint.before_request
@login_required
def check_survey_state():
    g.schema_json, g.schema = get_schema()
    values = request.view_args

    if not _same_survey(values['eq_id'], values['form_type'], values['collection_id']):
        return redirect(url_for('root.information', message_identifier='multiple-surveys'))


@questionnaire_blueprint.after_request
def add_cache_control(response):
    response.cache_control.no_cache = True
    return response


@questionnaire_blueprint.route('<group_id>/<int:group_instance>/<block_id>', methods=["GET"])
@login_required
def get_block(eq_id, form_type, collection_id, group_id, group_instance, block_id):
    # Filter answers down to those we may need to render
    answer_store = get_answer_store(current_user)
    answers = answer_store.map(group_id=group_id, group_instance=group_instance, block_id=block_id)

    this_block = {
        'group_id': group_id,
        'group_instance': group_instance,
        'block_id': block_id,
    }

    q_manager = get_questionnaire_manager(g.schema, g.schema_json)
    q_manager.build_state(this_block, answers)

    block = g.schema.get_item_by_id(block_id)
    template = block.type if block and block.type else 'questionnaire'

    return _render_template(q_manager.state, group_id, group_instance, block_id, template=template)


@questionnaire_blueprint.route('<group_id>/<int:group_instance>/<block_id>', methods=["POST"])
@login_required
def post_block(eq_id, form_type, collection_id, group_id, group_instance, block_id):
    navigator = Navigator(g.schema_json, get_metadata(current_user), get_answer_store(current_user))
    q_manager = get_questionnaire_manager(g.schema, g.schema_json)

    this_block = {
        'group_id': group_id,
        'group_instance': group_instance,
        'block_id': block_id,
    }

    valid_location = this_block in navigator.get_location_path()
    valid_data = q_manager.validate(this_block, request.form)

    if not valid_location or not valid_data:
        return _render_template(q_manager.state, group_id, group_instance, block_id, template='questionnaire')
    else:
        q_manager.update_questionnaire_store(this_block)

    navigator.update_answer_store(get_answer_store(current_user))

    next_location = navigator.get_next_location(current_group_id=group_id, current_iteration=group_instance, current_block_id=block_id)

    if next_location is None:
        raise NotFound

    metadata = get_metadata(current_user)

    if next_location['block_id'] == 'confirmation':
        return redirect_to_confirmation(eq_id, form_type, collection_id)

    logger.info("Redirecting user to next location %s with tx_id=%s", str(next_location), metadata["tx_id"])

    return redirect(block_url(eq_id, form_type, collection_id, next_location['group_id'], next_location['group_instance'], next_location['block_id']))


@questionnaire_blueprint.route('introduction', methods=["GET"])
@login_required
def get_introduction(eq_id, form_type, collection_id):
    return _render_template(get_introduction_context(g.schema_json), block_id='introduction')


@questionnaire_blueprint.route('<block_id>', methods=["POST"])
@login_required
def post_interstitial(eq_id, form_type, collection_id, block_id):
    navigator = Navigator(g.schema_json, get_metadata(current_user), get_answer_store(current_user))
    q_manager = get_questionnaire_manager(g.schema, g.schema_json)

    this_block = {
        'block_id': block_id,
        'group_id': SchemaHelper.get_first_group_id(g.schema_json),
        'group_instance': 0,
    }

    valid_location = this_block in navigator.get_location_path()
    q_manager.process_incoming_answers(this_block, request.form)

    # Don't care if data is valid because there isn't any for interstitial
    if not valid_location:
        return _render_template(q_manager.state, this_block['group_id'], this_block['group_instance'], block_id, template='questionnaire')

    next_location = navigator.get_next_location(current_block_id=block_id, current_iteration=0, current_group_id=this_block['group_id'])
    metadata = get_metadata(current_user)

    if next_location is None:
        raise NotFound

    logger.info("Redirecting user to next location %s with tx_id=%s", str(next_location), metadata["tx_id"])

    return redirect(block_url(eq_id, form_type, collection_id,
                              group_id=next_location['group_id'],
                              group_instance=next_location['group_instance'],
                              block_id=next_location['block_id']))


@questionnaire_blueprint.route('summary', methods=["GET"])
@login_required
def get_summary(eq_id, form_type, collection_id):

    answer_store = get_answer_store(current_user)
    navigator = Navigator(g.schema_json, get_metadata(current_user), answer_store)
    latest_location = navigator.get_latest_location(get_completed_blocks(current_user))

    if latest_location['block_id'] is 'summary':
        metadata = get_metadata(current_user)
        answers = get_answer_store(current_user)
        schema_context = build_schema_context(metadata, g.schema.aliases, answers)
        rendered_schema_json = renderer.render(g.schema_json, **schema_context)
        summary_context = build_summary_rendering_context(rendered_schema_json, answer_store, metadata)
        return _render_template(summary_context,
                                group_id=latest_location['group_id'],
                                group_instance=latest_location['group_instance'],
                                block_id=latest_location['block_id'])

    return redirect(block_url(eq_id, form_type, collection_id,
                              group_id=latest_location['group_id'],
                              group_instance=latest_location['group_instance'],
                              block_id=latest_location['block_id']))


@questionnaire_blueprint.route('confirmation', methods=["GET"])
@login_required
def get_confirmation(eq_id, form_type, collection_id):
    navigator = Navigator(g.schema_json, get_metadata(current_user), get_answer_store(current_user))

    latest_location = navigator.get_latest_location(get_completed_blocks(current_user))

    if latest_location['block_id'] == 'confirmation':
        q_manager = get_questionnaire_manager(g.schema, g.schema_json)

        return _render_template(q_manager.state,
                                group_id=latest_location['group_id'],
                                group_instance=latest_location['group_instance'],
                                block_id=latest_location['block_id'])

    return redirect(block_url(eq_id, form_type, collection_id,
                              group_id=latest_location['group_id'],
                              group_instance=latest_location['group_instance'],
                              block_id=latest_location['block_id']))


@questionnaire_blueprint.route('thank-you', methods=["GET"])
@login_required
def get_thank_you(eq_id, form_type, collection_id):
    if not _same_survey(eq_id, form_type, collection_id):
        return redirect("/information/multiple-surveys")

    thank_you_page = _render_template(get_questionnaire_manager(g.schema, g.schema_json).state, block_id='thank-you')
    # Delete user data on request of thank you page.
    _delete_user_data()
    return thank_you_page


@questionnaire_blueprint.route('submit-answers', methods=["POST"])
@login_required
def submit_answers(eq_id, form_type, collection_id):
    q_manager = get_questionnaire_manager(g.schema, g.schema_json)
    # check that all the answers we have are valid before submitting the data
    is_valid, invalid_location = q_manager.validate_all_answers()

    if is_valid:
        metadata = get_metadata(current_user)
        answer_store = get_answer_store(current_user)
        navigator = Navigator(g.schema_json, metadata, answer_store)
        submitter = SubmitterFactory.get_submitter()
        message = convert_answers(metadata, g.schema, answer_store, navigator.get_routing_path())
        submitter.send_answers(message)
        logger.info("Responses submitted tx_id=%s", metadata["tx_id"])
        return redirect_to_thank_you(eq_id, form_type, collection_id)
    else:
        return redirect(block_url(eq_id, form_type, collection_id,
                                  group_id=invalid_location['group_id'],
                                  group_instance=invalid_location['group_instance'],
                                  block_id=invalid_location['block_id']))


@questionnaire_blueprint.route('<group_id>/0/household-composition', methods=["POST"])
@login_required
def post_household_composition(eq_id, form_type, collection_id, group_id):
    questionnaire_manager = get_questionnaire_manager(g.schema, g.schema_json)
    answer_store = get_answer_store(current_user)

    this_block = {
        'block_id': 'household-composition',
        'group_id': group_id,
        'group_instance': 0,
    }

    valid = questionnaire_manager.process_incoming_answers(this_block, request.form)

    if 'action[add_answer]' in request.form:
        questionnaire_manager.add_answer(this_block, 'household-composition-question', answer_store)
        return get_block(eq_id, form_type, collection_id, group_id, 0, 'household-composition')

    elif 'action[remove_answer]' in request.form:
        index_to_remove = request.form.get('action[remove_answer]')
        questionnaire_manager.remove_answer(this_block, answer_store, index_to_remove)
        return get_block(eq_id, form_type, collection_id, group_id, 0, 'household-composition')

    if not valid:
        return _render_template(questionnaire_manager.state, group_id, 0, 'household-composition', template='questionnaire')

    return _go_to_next_block(location=this_block, eq_id=eq_id,
                             form_type=form_type, collection_id=collection_id)


def _go_to_next_block(location, eq_id, form_type, collection_id):
    navigator = Navigator(g.schema_json, get_metadata(current_user), get_answer_store(current_user))

    next_location = navigator.get_next_location(current_block_id=location['block_id'],
                                                current_group_id=location['group_id'],
                                                current_iteration=location['group_instance'])

    if next_location is None:
        raise NotFound

    metadata = get_metadata(current_user)
    logger.info("Redirecting user to next location %s with tx_id=%s", next_location, metadata["tx_id"])
    return redirect(block_url(eq_id, form_type, collection_id,
                              group_id=next_location['group_id'],
                              group_instance=next_location['group_instance'],
                              block_id=next_location['block_id']))


def _delete_user_data():
    get_questionnaire_store(current_user.user_id, current_user.user_ik).delete()
    session_manager.clear()


def redirect_to_summary(eq_id, form_type, collection_id):
    return redirect(interstitial_url(eq_id, form_type, collection_id, 'summary'))


def redirect_to_thank_you(eq_id, form_type, collection_id):
    return redirect(interstitial_url(eq_id, form_type, collection_id, 'thank-you'))


def redirect_to_confirmation(eq_id, form_type, collection_id):
    return redirect(interstitial_url(eq_id, form_type, collection_id, 'confirmation'))


def interstitial_url(eq_id, form_type, collection_id, block_id):
    if block_id == 'summary':
        return url_for('.get_summary',
                       eq_id=eq_id,
                       form_type=form_type,
                       collection_id=collection_id)
    elif block_id == 'introduction':
        return url_for('.get_introduction',
                       eq_id=eq_id,
                       form_type=form_type,
                       collection_id=collection_id)
    elif block_id == 'confirmation':
        return url_for('.get_confirmation',
                       eq_id=eq_id,
                       form_type=form_type,
                       collection_id=collection_id)
    elif block_id == 'thank-you':
        return url_for('.get_thank_you',
                       eq_id=eq_id,
                       form_type=form_type,
                       collection_id=collection_id)


def block_url(eq_id, form_type, collection_id, group_id, group_instance, block_id):
    if Navigator.is_interstitial_block(block_id):
        return interstitial_url(eq_id, form_type, collection_id, block_id)
    return url_for('.get_block',
                   eq_id=eq_id,
                   form_type=form_type,
                   collection_id=collection_id,
                   group_id=group_id,
                   group_instance=group_instance,
                   block_id=block_id)


def _same_survey(eq_id, form_type, collection_id):
    metadata = get_metadata(current_user)
    current_survey = eq_id + form_type + collection_id
    metadata_survey = metadata["eq_id"] + metadata["form_type"] + metadata["collection_exercise_sid"]
    return current_survey == metadata_survey


def _render_template(context, group_id=None, group_instance=0, block_id=None, template=None):
    metadata = get_metadata(current_user)
    metadata_context = build_metadata_context(metadata)

    navigator = Navigator(g.schema_json, get_metadata(current_user), get_answer_store(current_user))
    group_id = group_id or SchemaHelper.get_first_group_id(g.schema_json)

    previous_location = navigator.get_previous_location(current_group_id=group_id,
                                                        current_block_id=block_id,
                                                        current_iteration=group_instance)

    previous_url = None

    if previous_location is not None:
        previous_url = block_url(eq_id=metadata['eq_id'],
                                 form_type=metadata['form_type'],
                                 collection_id=metadata['collection_exercise_sid'],
                                 group_id=previous_location['group_id'],
                                 group_instance=previous_location['group_instance'],
                                 block_id=previous_location['block_id'])

    try:
        theme = g.schema_json['theme']
        logger.debug("Theme selected: %s", theme)
    except KeyError:
        logger.info("No theme set")
        theme = None

    template = '{}.html'.format(template or block_id)

    return render_theme_template(theme, template, meta=metadata_context,
                                 content=context,
                                 previous_location=previous_url,
                                 schema=g.schema_json)

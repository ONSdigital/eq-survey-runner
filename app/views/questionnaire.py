import re

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
from app.data_model.answer_store import Answer
from app.globals import get_answer_store, get_completed_blocks, get_metadata, get_questionnaire_store
from app.helpers.form_helper import get_form_for_location, post_form_for_location
from app.helpers.schema_helper import SchemaHelper
from app.questionnaire.location import Location
from app.questionnaire.navigation import Navigation
from app.questionnaire.path_finder import PathFinder
from app.questionnaire.rules import evaluate_skip_condition
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
    g.schema_json = get_schema(get_metadata(current_user))
    values = request.view_args
    logger.debug('questionnaire request', eq_id=values['eq_id'], form_type=values['form_type'],
                 ce_id=values['collection_id'], method=request.method, url_path=request.full_path)

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
    path_finder = PathFinder(g.schema_json, answer_store, get_metadata(current_user))

    current_location = Location(group_id, group_instance, block_id)

    valid_group = group_id in SchemaHelper.get_group_ids(g.schema_json)

    if not valid_group or current_location not in path_finder.get_routing_path(group_id, group_instance):
        raise NotFound

    block = _render_schema(current_location)

    error_messages = SchemaHelper.get_messages(g.schema_json)
    form, template_params = get_form_for_location(block, current_location, answer_store, error_messages)

    content = {'form': form, 'block': block}

    if template_params:
        content.update(template_params)

    template = block['type'] if block and 'type' in block and block['type'] else 'questionnaire'

    return _build_template(current_location, content, template)


@questionnaire_blueprint.route('<group_id>/<int:group_instance>/<block_id>', methods=["POST"])
@login_required
def post_block(eq_id, form_type, collection_id, group_id, group_instance, block_id):
    path_finder = PathFinder(g.schema_json, get_answer_store(current_user), get_metadata(current_user))

    current_location = Location(group_id, group_instance, block_id)

    valid_location = current_location in path_finder.get_routing_path(group_id, group_instance)

    block = _render_schema(current_location)

    error_messages = SchemaHelper.get_messages(g.schema_json)

    disable_mandatory = 'action[save_sign_out]' in request.form

    form, _ = post_form_for_location(block, current_location, get_answer_store(current_user),
                                     request.form, error_messages, disable_mandatory=disable_mandatory)

    if 'action[save_sign_out]' in request.form:
        return _save_sign_out(collection_id, eq_id, form_type, current_location, form)

    content = {
        'form': form,
        'block': block,
    }

    if not valid_location or not form.validate():
        return _build_template(current_location, content, template='questionnaire')
    else:
        questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)

        if current_location.block_id in ['relationships', 'household-relationships']:
            update_questionnaire_store_with_answer_data(questionnaire_store, current_location, form.serialise(current_location))
        else:
            update_questionnaire_store_with_form_data(questionnaire_store, current_location, form.data)

    next_location = path_finder.get_next_location(current_location=current_location)

    if next_location is None:
        raise NotFound

    metadata = get_metadata(current_user)

    return redirect(next_location.url(metadata))


@questionnaire_blueprint.route('<group_id>/0/household-composition', methods=["POST"])
@login_required
def post_household_composition(eq_id, form_type, collection_id, group_id):
    path_finder = PathFinder(g.schema_json, get_answer_store(current_user), get_metadata(current_user))
    answer_store = get_answer_store(current_user)
    questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)

    current_location = Location(group_id, 0, 'household-composition')
    block = _render_schema(current_location)

    if _household_answers_changed(answer_store):
        _remove_repeating_on_household_answers(answer_store, group_id)

    error_messages = SchemaHelper.get_messages(g.schema_json)

    if any(x in request.form for x in ['action[add_answer]', 'action[remove_answer]', 'action[save_sign_out]']):
        disable_mandatory = True
    else:
        disable_mandatory = False

    form, _ = post_form_for_location(block, current_location, answer_store,
                                     request.form, error_messages, disable_mandatory=disable_mandatory)

    if 'action[add_answer]' in request.form:
        form.household.append_entry()
    elif 'action[remove_answer]' in request.form:
        index_to_remove = int(request.form.get('action[remove_answer]'))

        form.remove_person(index_to_remove)
    elif 'action[save_sign_out]' in request.form:
        return _save_sign_out(collection_id, eq_id, form_type, current_location, form)

    if not form.validate() or 'action[add_answer]' in request.form or 'action[remove_answer]' in request.form:
        return _render_template({
            'form': form,
            'block': block,
        }, current_location.block_id, current_location=current_location, template='questionnaire')

    update_questionnaire_store_with_answer_data(questionnaire_store, current_location, form.serialise(current_location))

    next_location = path_finder.get_next_location(current_location=current_location)

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

    current_location = Location(SchemaHelper.get_first_group_id(g.schema_json), 0, block_id)

    valid_location = current_location in path_finder.get_location_path()
    questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)
    update_questionnaire_store_with_form_data(questionnaire_store, current_location, request.form.to_dict())

    # Don't care if data is valid because there isn't any for interstitial
    if not valid_location:
        block = _render_schema(current_location)
        return _build_template(current_location=current_location, context={"block": block}, template='questionnaire')

    next_location = path_finder.get_next_location(current_location=current_location)

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
        aliases = SchemaHelper.get_aliases(g.schema_json)
        schema_context = build_schema_context(metadata, aliases, answer_store)
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
        block = _render_schema(latest_location)
        return _build_template(current_location=latest_location, context={"block": block})

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
    signed_out_page = _render_template({}, block_id='signed-out')
    session_storage.clear()
    return signed_out_page


@questionnaire_blueprint.route('submit-answers', methods=["POST"])
@login_required
def submit_answers(eq_id, form_type, collection_id):
    metadata = get_metadata(current_user)

    answer_store = get_answer_store(current_user)

    is_valid, invalid_location = validate_all_answers(answer_store, metadata)

    if is_valid:
        path_finder = PathFinder(g.schema_json, answer_store, metadata)
        submitter = SubmitterFactory.get_submitter()
        message = convert_answers(metadata, g.schema_json, answer_store, path_finder.get_routing_path())
        message['completed'] = True
        submitter.send_answers(message)

        return redirect(url_for('.get_thank_you', eq_id=eq_id, form_type=form_type, collection_id=collection_id))
    else:
        return redirect(invalid_location.url(metadata))


@questionnaire_blueprint.route('<group_id>/<int:group_instance>/permanent-or-family-home', methods=["POST"])
@login_required
def post_everyone_at_address_confirmation(eq_id, form_type, collection_id, group_id, group_instance):
    if request.form.get('permanent-or-family-home-answer') == 'No':
        _remove_repeating_on_household_answers(get_answer_store(current_user), group_id)
    return post_block(eq_id, form_type, collection_id, group_id, group_instance, 'permanent-or-family-home')


def validate_all_answers(answer_store, metadata):

    path_finder = PathFinder(g.schema_json, answer_store, metadata)
    error_messages = SchemaHelper.get_messages(g.schema_json)

    for location in path_finder.get_location_path():
        if not location.is_interstitial():
            block_json = _render_schema(location)
            form, _ = get_form_for_location(block_json, location, answer_store, error_messages)

            if not form.validate():
                logger.debug("Failed validation", location=str(location))
                return False, location

    return True, None


def _save_sign_out(collection_id, eq_id, form_type, this_location, form):
    questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)

    block_json = _render_schema(this_location)

    # Form will have been created with no mandatory fields
    if not form.validate():
        content = {'block': block_json, 'form': form}
        return _build_template(this_location, content, template='questionnaire')
    else:
        if this_location.block_id != 'household-composition':
            update_questionnaire_store_with_form_data(questionnaire_store, this_location, form.data)
        else:
            update_questionnaire_store_with_answer_data(questionnaire_store, this_location, form.serialise(this_location))

        if this_location in questionnaire_store.completed_blocks:
            questionnaire_store.completed_blocks.remove(this_location)
        return redirect(url_for('.get_sign_out', eq_id=eq_id, form_type=form_type, collection_id=collection_id))


def _household_answers_changed(answer_store):
    household_answers = answer_store.filter(block_id="household-composition")
    if len(household_answers) != len(request.form)-1:
        return True
    for answer in request.form:
        answer_id, answer_index = extract_answer_id_and_instance(answer)

        stored_answer = next((d for d in household_answers if d['answer_id'] == answer_id and
                              d['answer_instance'] == answer_index), None)
        if stored_answer and (stored_answer['value'] or '') != request.form[answer]:
            return True
    return False


def _remove_repeating_on_household_answers(answer_store, group_id):
    answer_store.remove(group_id=group_id, block_id='household-composition')
    questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)
    for answer in SchemaHelper.get_answers_that_repeat_in_block(g.schema_json, 'household-composition'):
        groups_to_delete = SchemaHelper.get_groups_that_repeat_with_answer_id(g.schema_json, answer['id'])
        for group in groups_to_delete:
            answer_store.remove(group_id=group['id'])
            questionnaire_store.completed_blocks[:] = [b for b in questionnaire_store.completed_blocks if
                                                       b.group_id != group['id']]


def update_questionnaire_store_with_form_data(questionnaire_store, location, answer_dict):

    survey_answer_ids = SchemaHelper.get_answer_ids_for_location(g.schema_json, location)

    for answer_id, answer_value in answer_dict.items():
        if answer_id in survey_answer_ids or location.block_id == 'household-composition':
            answer = None
            # Dates are comprised of 3 string values

            if isinstance(answer_value, dict):
                is_day_month_year = 'day' in answer_value and 'month' in answer_value
                is_month_year = 'year' in answer_value and 'month' in answer_value

                if is_day_month_year and answer_value['day'] and answer_value['month']:
                    date_str = "{:02d}/{:02d}/{}".format(
                        int(answer_value['day']),
                        int(answer_value['month']),
                        answer_value['year'],
                    )
                    answer = Answer(answer_id=answer_id, value=date_str, location=location)
                elif is_month_year and answer_value['month']:
                    date_str = "{:02d}/{}".format(int(answer_value['month']), answer_value['year'])
                    answer = Answer(answer_id=answer_id, value=date_str, location=location)
            elif answer_value != 'None' and answer_value is not None:
                # Necessary because default select casts to string value 'None'
                answer = Answer(answer_id=answer_id, value=answer_value, location=location)

            if answer:
                questionnaire_store.answer_store.add_or_update(answer)

    if location not in questionnaire_store.completed_blocks:
        questionnaire_store.completed_blocks.append(location)


def update_questionnaire_store_with_answer_data(questionnaire_store, location, answers):

    survey_answer_ids = SchemaHelper.get_answer_ids_for_location(g.schema_json, location)

    for answer in [a for a in answers if a.answer_id in survey_answer_ids]:
        questionnaire_store.answer_store.add_or_update(answer)

    if location not in questionnaire_store.completed_blocks:
        questionnaire_store.completed_blocks.append(location)


def _delete_user_data():
    get_questionnaire_store(current_user.user_id, current_user.user_ik).delete()
    session_storage.clear()


def _check_same_survey(eq_id, form_type, collection_id):
    metadata = get_metadata(current_user)
    current_survey = eq_id + form_type + collection_id
    metadata_survey = metadata["eq_id"] + metadata["form_type"] + metadata["collection_exercise_sid"]
    if current_survey != metadata_survey:
        raise MultipleSurveyError


def _evaluate_skip_conditions(block_json, location, answer_store, metadata):
    for question in SchemaHelper.get_questions_for_block(block_json):
        if 'skip_condition' in question:
            skip_question = evaluate_skip_condition([question['skip_condition']], metadata, answer_store,
                                                    location.group_instance)
            question['skipped'] = skip_question

            for answer in question['answers']:
                if answer['mandatory'] and skip_question:
                    answer['mandatory'] = False

    return block_json


def extract_answer_id_and_instance(answer_instance_id):
    matches = re.match(r'^household-(\d+)-(first-name|middle-names|last-name)$', answer_instance_id)

    if matches:
        index, answer_id = matches.groups()
    else:
        answer_id = answer_instance_id
        index = 0

    return answer_id, int(index)


def _render_schema(current_location):
    metadata = get_metadata(current_user)
    answer_store = get_answer_store(current_user)
    block_json = SchemaHelper.get_block_for_location(g.schema_json, current_location)
    block_json = _evaluate_skip_conditions(block_json, current_location, answer_store, metadata)
    aliases = SchemaHelper.get_aliases(g.schema_json)
    block_context = build_schema_context(metadata, aliases, answer_store, current_location.group_instance)
    return renderer.render(block_json, **block_context)


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

    return _render_template(context, current_location.block_id, front_end_navigation, metadata_context, current_location, previous_url, template)


def _render_template(context, block_id, front_end_navigation=None, metadata_context=None, current_location=None, previous_url=None, template=None):
    theme = g.schema_json.get('theme', None)
    logger.debug("theme selected", theme=theme)
    template = '{}.html'.format(template or block_id)
    return render_theme_template(theme, template,
                                 meta=metadata_context,
                                 content=context,
                                 current_location=current_location,
                                 previous_location=previous_url,
                                 navigation=front_end_navigation,
                                 schema_title=g.schema_json['title'],
                                 legal_basis=g.schema_json['legal_basis'],
                                 survey_id=g.schema_json['survey_id'],)

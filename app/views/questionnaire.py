import re
from collections import defaultdict

from flask import Blueprint
from flask import g
from flask import redirect
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import logout_user
from flask_themes2 import render_theme_template
from structlog import get_logger

from app import settings
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
    g.schema_json = get_schema(metadata)
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
    current_location = Location(group_id, group_instance, block_id)
    metadata = get_metadata(current_user)
    answer_store = get_answer_store(current_user)
    path_finder = PathFinder(g.schema_json, answer_store, metadata)

    valid_group = group_id in SchemaHelper.get_group_ids(g.schema_json)
    is_valid_location = valid_group and current_location in path_finder.get_routing_path(group_id, group_instance)
    latest_location = path_finder.get_latest_location(get_completed_blocks(current_user))
    if not is_valid_location:
        return _redirect_to_latest_location(collection_id, eq_id, form_type, latest_location)

    block = _render_schema(current_location)
    block_type = block['type']
    is_skipping_to_end = block_type in ['Summary', 'Confirmation'] and current_location != latest_location
    if is_skipping_to_end:
        return _redirect_to_latest_location(collection_id, eq_id, form_type, latest_location)

    context = _get_context(block, current_location, answer_store)
    return _build_template(current_location, context, template=block_type)


@questionnaire_blueprint.route('<group_id>/<int:group_instance>/<block_id>', methods=["POST"])
@login_required
def post_block(eq_id, form_type, collection_id, group_id, group_instance, block_id):
    current_location = Location(group_id, group_instance, block_id)
    metadata = get_metadata(current_user)
    answer_store = get_answer_store(current_user)
    path_finder = PathFinder(g.schema_json, answer_store, metadata)

    valid_group = group_id in SchemaHelper.get_group_ids(g.schema_json)
    is_valid_location = valid_group and current_location in path_finder.get_routing_path(group_id, group_instance)
    if not is_valid_location:
        latest_location = path_finder.get_latest_location(get_completed_blocks(current_user))
        return _redirect_to_latest_location(collection_id, eq_id, form_type, latest_location)

    error_messages = SchemaHelper.get_messages(g.schema_json)
    block = _render_schema(current_location)
    disable_mandatory = 'action[save_sign_out]' in request.form
    form, _ = post_form_for_location(block, current_location, answer_store, request.form, error_messages, disable_mandatory=disable_mandatory)

    if 'action[save_sign_out]' in request.form:
        return _save_sign_out(collection_id, eq_id, form_type, current_location, form)
    elif not form.validate():
        context = {'form': form, 'block': block}
        return _build_template(current_location, context, template=block['type'])
    else:
        _update_questionnaire_store(current_location, form)
        next_location = path_finder.get_next_location(current_location=current_location)
        return redirect(next_location.url(metadata))


@questionnaire_blueprint.route('<group_id>/0/household-composition', methods=["POST"])
@login_required
def post_household_composition(eq_id, form_type, collection_id, group_id):
    answer_store = get_answer_store(current_user)
    if _household_answers_changed(answer_store):
        _remove_repeating_on_household_answers(answer_store, group_id)

    if any(x in request.form for x in ['action[add_answer]', 'action[remove_answer]', 'action[save_sign_out]']):
        disable_mandatory = True
    else:
        disable_mandatory = False

    error_messages = SchemaHelper.get_messages(g.schema_json)
    current_location = Location(group_id, 0, 'household-composition')
    block = _render_schema(current_location)
    form, _ = post_form_for_location(block, current_location, answer_store, request.form, error_messages, disable_mandatory=disable_mandatory)

    if 'action[add_answer]' in request.form:
        form.household.append_entry()
    elif 'action[remove_answer]' in request.form:
        index_to_remove = int(request.form.get('action[remove_answer]'))
        form.remove_person(index_to_remove)
    elif 'action[save_sign_out]' in request.form:
        response = _save_sign_out(collection_id, eq_id, form_type, current_location, form)
        remove_empty_household_members_from_answer_store(answer_store, group_id)
        return response

    if not form.validate() or 'action[add_answer]' in request.form or 'action[remove_answer]' in request.form:
        context = {'form': form, 'block': block}
        return _build_template(current_location, context, template='questionnaire')
    else:
        questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)
        update_questionnaire_store_with_answer_data(questionnaire_store, current_location, form.serialise(current_location))

        metadata = get_metadata(current_user)
        path_finder = PathFinder(g.schema_json, get_answer_store(current_user), metadata)
        next_location = path_finder.get_next_location(current_location=current_location)
        return redirect(next_location.url(metadata))


@questionnaire_blueprint.route('thank-you', methods=["GET"])
@login_required
def get_thank_you(eq_id, form_type, collection_id):  # pylint: disable=unused-argument
    theme = g.schema_json.get('theme', None)
    logger.debug("theme selected", theme=theme)
    metadata = get_metadata(current_user)
    metadata_context = build_metadata_context(metadata)
    thank_you_template = render_theme_template(theme, template_name='thank-you.html',
                                               meta=metadata_context,
                                               schema_title=g.schema_json['title'],
                                               legal_basis=g.schema_json['legal_basis'],
                                               analytics_ua_id=settings.EQ_UA_ID,
                                               survey_id=g.schema_json['survey_id'])
    _delete_user_data()
    return thank_you_template


@questionnaire_blueprint.route('signed-out', methods=["GET"])
@login_required
def get_sign_out(eq_id, form_type, collection_id):  # pylint: disable=unused-argument
    theme = g.schema_json.get('theme', None)
    logger.debug("theme selected", theme=theme)
    signed_out_template = render_theme_template(theme, template_name='signed-out.html',
                                                schema_title=g.schema_json['title'],
                                                legal_basis=g.schema_json['legal_basis'],
                                                analytics_ua_id=settings.EQ_UA_ID,
                                                survey_id=g.schema_json['survey_id'])
    session_storage.clear()
    return signed_out_template


@questionnaire_blueprint.route('timeout-continue', methods=["GET"])
@login_required
def get_timeout_continue(eq_id, form_type, collection_id):  # pylint: disable=unused-argument
    return 'true'


@questionnaire_blueprint.route('session-expired', methods=["GET"])
@login_required
def get_session_expired(eq_id, form_type, collection_id):  # pylint: disable=unused-argument
    _delete_user_data()
    theme = g.schema_json.get('theme', None)
    logger.debug("theme selected", theme=theme)
    return render_theme_template(theme, template_name='session-expired.html',
                                 schema_title=g.schema_json['title'],
                                 legal_basis=g.schema_json['legal_basis'],
                                 analytics_ua_id=settings.EQ_UA_ID,
                                 survey_id=g.schema_json['survey_id'])


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

    for location in path_finder.get_routing_path():
        block_json = _render_schema(location)
        form, _ = get_form_for_location(block_json, location, answer_store, error_messages)

        if not form.validate():
            logger.debug("Failed validation", location=str(location))
            return False, location

    return True, None


def _save_sign_out(collection_id, eq_id, form_type, this_location, form):
    questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)
    block_json = _render_schema(this_location)

    if not form.validate():
        content = {'block': block_json, 'form': form}
        return _build_template(this_location, content, template=block_json['type'])
    else:
        _update_questionnaire_store(this_location, form)

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


def remove_empty_household_members_from_answer_store(answer_store, group_id):
    household_answers = answer_store.filter(group_id=group_id, block_id='household-composition')
    household_member_name = defaultdict(list)
    for household_answer in household_answers:
        if household_answer['answer_id'] == 'first-name' or household_answer['answer_id'] == 'last-name':
            household_member_name[household_answer['answer_instance']].append(household_answer['value'])

    to_be_removed = []
    for k, v in household_member_name.items():
        name_value = ''.join(v).strip()
        if not name_value:
            to_be_removed.append(k)

    for instance_to_remove in to_be_removed:
        answer_store.remove(group_id=group_id, block_id='household-composition', answer_instance=instance_to_remove)


def _update_questionnaire_store(current_location, form):
    questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)
    if current_location.block_id in ['relationships', 'household-relationships']:
        update_questionnaire_store_with_answer_data(questionnaire_store, current_location,
                                                    form.serialise(current_location))
    else:
        update_questionnaire_store_with_form_data(questionnaire_store, current_location, form.data)


def update_questionnaire_store_with_form_data(questionnaire_store, location, answer_dict):

    survey_answer_ids = SchemaHelper.get_answer_ids_for_location(g.schema_json, location)

    for answer_id, answer_value in answer_dict.items():
        if answer_id in survey_answer_ids or location.block_id == 'household-composition':
            answer = None

            # Dates are comprised of 3 string values
            if isinstance(answer_value, dict):
                is_day_month_year = 'day' in answer_value and 'month' in answer_value and 'year' in answer_value
                is_month_year = 'day' not in answer_value and 'year' in answer_value and 'month' in answer_value

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
            elif answer_value is None:
                # Remove previously populated answers that are now empty
                questionnaire_store.answer_store.remove(
                    location=location,
                    answer_id=answer_id,
                    answer_instance=0,
                )

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
    logout_user()


def _check_same_survey(eq_id, form_type, collection_id):
    metadata = get_metadata(current_user)
    current_survey = eq_id + form_type + collection_id
    metadata_survey = metadata["eq_id"] + metadata["form_type"] + metadata["collection_exercise_sid"]
    if current_survey != metadata_survey:
        raise MultipleSurveyError


def _evaluate_skip_conditions(block_json, location, answer_store, metadata):
    for question in SchemaHelper.get_questions_for_block(block_json):
        if 'skip_condition' in question:
            skip_question = evaluate_skip_condition([question['skip_condition']], metadata, answer_store, location.group_instance)
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


def _redirect_to_latest_location(collection_id, eq_id, form_type, latest_location):
    return redirect(url_for('.get_block', eq_id=eq_id, form_type=form_type, collection_id=collection_id,
                            group_id=latest_location.group_id,
                            group_instance=latest_location.group_instance, block_id=latest_location.block_id))


def _get_context(block, current_location, answer_store):
    if block['type'] == 'Summary':
        metadata = get_metadata(current_user)
        aliases = SchemaHelper.get_aliases(g.schema_json)
        schema_context = build_schema_context(metadata, aliases, answer_store)
        rendered_schema_json = renderer.render(g.schema_json, **schema_context)
        return build_summary_rendering_context(rendered_schema_json, answer_store, metadata)
    else:
        error_messages = SchemaHelper.get_messages(g.schema_json)
        form, template_params = get_form_for_location(block, current_location, answer_store, error_messages)
        content = {'form': form, 'block': block}
        if template_params:
            content.update(template_params)
        return content


def _render_schema(current_location):
    metadata = get_metadata(current_user)
    answer_store = get_answer_store(current_user)
    block_json = SchemaHelper.get_block_for_location(g.schema_json, current_location)
    block_json = _evaluate_skip_conditions(block_json, current_location, answer_store, metadata)
    aliases = SchemaHelper.get_aliases(g.schema_json)
    block_context = build_schema_context(metadata, aliases, answer_store, current_location.group_instance)
    return renderer.render(block_json, **block_context)


def _get_front_end_navigation(answer_store, current_location, metadata):
    completed_blocks = get_completed_blocks(current_user)
    navigation = Navigation(g.schema_json, answer_store, metadata, completed_blocks)
    block_json = SchemaHelper.get_block_for_location(g.schema_json, current_location)
    if block_json is not None and (block_json['type'] == 'Questionnaire' or block_json['type'] == 'Interstitial'):
        return navigation.build_navigation(current_location.group_id, current_location.group_instance)
    else:
        return None


def _build_template(current_location, context, template):
    metadata = get_metadata(current_user)
    metadata_context = build_metadata_context(metadata)

    answer_store = get_answer_store(current_user)
    front_end_navigation = _get_front_end_navigation(answer_store, current_location, metadata)

    path_finder = PathFinder(g.schema_json, answer_store, metadata)
    previous_location = path_finder.get_previous_location(current_location)

    previous_url = previous_location.url(metadata) if previous_location is not None else None
    return _render_template(context, front_end_navigation, metadata_context, current_location, previous_url, template)


def _render_template(context, front_end_navigation=None, metadata_context=None, current_location=None, previous_url=None, template=None):
    theme = g.schema_json.get('theme', None)
    logger.debug("theme selected", theme=theme)
    session_timeout = settings.EQ_SESSION_TIMEOUT_SECONDS
    schema_session_timeout = g.schema_json.get('session_timeout_in_seconds')
    if schema_session_timeout is not None and schema_session_timeout < settings.EQ_SESSION_TIMEOUT_SECONDS:
        session_timeout = schema_session_timeout
    session_timeout_prompt = g.schema_json.get('session_prompt_in_seconds') or settings.EQ_SESSION_TIMEOUT_PROMPT_SECONDS

    if metadata_context is not None:
        survey_data = metadata_context['survey']
        url_prefix = '/questionnaire/{}/{}/{}'.format(survey_data['eq_id'], survey_data['form_type'], survey_data['collection_id'])
    else:
        url_prefix = None

    template = '{}.html'.format(template).lower()
    return render_theme_template(theme, template,
                                 meta=metadata_context,
                                 content=context,
                                 current_location=current_location,
                                 analytics_ua_id=settings.EQ_UA_ID,
                                 previous_location=previous_url,
                                 navigation=front_end_navigation,
                                 schema_title=g.schema_json['title'],
                                 legal_basis=g.schema_json['legal_basis'],
                                 survey_id=g.schema_json['survey_id'],
                                 session_timeout=session_timeout,
                                 session_timeout_prompt=session_timeout_prompt,
                                 url_prefix=url_prefix)

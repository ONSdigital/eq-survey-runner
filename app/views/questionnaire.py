import re
from collections import defaultdict

from flask import Blueprint, g, redirect, request, url_for, current_app
from flask_login import current_user, login_required, logout_user
from flask_themes2 import render_theme_template
from structlog import get_logger
from werkzeug.exceptions import Forbidden

from app.data_model.answer_store import Answer
from app.globals import get_answer_store, get_completed_blocks, get_metadata, get_questionnaire_store
from app.helpers.form_helper import get_form_for_location, post_form_for_location
from app.helpers.schema_helper import SchemaHelper
from app.questionnaire.location import Location
from app.questionnaire.navigation import Navigation
from app.questionnaire.path_finder import PathFinder
from app.questionnaire.rules import evaluate_skip_condition
from app.submitter.converter import convert_answers
from app.submitter.submission_failed import SubmissionFailedException
from app.templating.metadata_context import build_metadata_context, build_metadata_context_for_survey_completed
from app.templating.schema_context import build_schema_context
from app.templating.summary_context import build_summary_rendering_context
from app.templating.template_renderer import renderer, TemplateRenderer
from app.utilities.schema import load_schema_from_metadata, load_schema_from_params
from app.views.errors import MultipleSurveyError

logger = get_logger()

questionnaire_blueprint = Blueprint(name='questionnaire',
                                    import_name=__name__,
                                    url_prefix='/questionnaire/<eq_id>/<form_type>/<collection_id>/')


@questionnaire_blueprint.before_request
def before_request():
    values = request.view_args
    logger.info('questionnaire request', eq_id=values['eq_id'], form_type=values['form_type'],
                ce_id=values['collection_id'], method=request.method, url_path=request.full_path)

    metadata = get_metadata(current_user)
    if metadata:
        logger.bind(tx_id=metadata['tx_id'])
        g.schema_json = load_schema_from_metadata(metadata)
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
def get_block(eq_id, form_type, collection_id, group_id, group_instance, block_id):  # pylint: disable=unused-argument,too-many-locals
    current_location = Location(group_id, group_instance, block_id)
    metadata = get_metadata(current_user)
    answer_store = get_answer_store(current_user)
    path_finder = PathFinder(g.schema_json, answer_store, metadata)
    valid_group = group_id in SchemaHelper.get_group_ids(g.schema_json)
    full_routing_path = path_finder.get_routing_path()
    is_valid_location = valid_group and current_location in path_finder.get_routing_path(group_id, group_instance)
    latest_location = path_finder.get_latest_location(get_completed_blocks(current_user), routing_path=full_routing_path)
    if not is_valid_location:
        return _redirect_to_location(collection_id, eq_id, form_type, latest_location)

    block = _render_schema(current_location)
    block_type = block['type']
    is_skipping_to_end = block_type in ['Summary', 'Confirmation'] and current_location != latest_location
    if is_skipping_to_end:
        return _redirect_to_location(collection_id, eq_id, form_type, latest_location)

    context = _get_context(block, current_location, answer_store)
    return _build_template(current_location, context, template=block_type, routing_path=full_routing_path)


@questionnaire_blueprint.route('<group_id>/<int:group_instance>/<block_id>', methods=["POST"])
@login_required
def post_block(eq_id, form_type, collection_id, group_id, group_instance, block_id):  # pylint: disable=too-many-locals
    current_location = Location(group_id, group_instance, block_id)
    metadata = get_metadata(current_user)
    answer_store = get_answer_store(current_user)
    path_finder = PathFinder(g.schema_json, answer_store, metadata)

    valid_group = group_id in SchemaHelper.get_group_ids(g.schema_json)
    full_routing_path = path_finder.get_routing_path()
    is_valid_location = valid_group and current_location in path_finder.get_routing_path(group_id, group_instance)
    if not is_valid_location:
        latest_location = path_finder.get_latest_location(get_completed_blocks(current_user), routing_path=full_routing_path)
        return _redirect_to_location(collection_id, eq_id, form_type, latest_location)

    error_messages = SchemaHelper.get_messages(g.schema_json)
    block = _render_schema(current_location)
    disable_mandatory = 'action[save_sign_out]' in request.form
    form, _ = post_form_for_location(block, current_location, answer_store, request.form, error_messages, disable_mandatory=disable_mandatory)

    if 'action[save_sign_out]' in request.form:
        return _save_sign_out(collection_id, eq_id, form_type, current_location, form)
    elif _is_invalid_form(form):
        context = {'form': form, 'block': block}
        return _build_template(current_location, context, template=block['type'], routing_path=full_routing_path)
    else:
        _update_questionnaire_store(current_location, form)
        next_location = path_finder.get_next_location(current_location=current_location)

        if next_location is None and block['type'] in ["Summary", "Confirmation"]:
            return submit_answers(eq_id, form_type, collection_id, metadata, answer_store)

        return redirect(next_location.url(metadata))


@questionnaire_blueprint.route('<group_id>/0/household-composition', methods=["POST"])
@login_required
def post_household_composition(eq_id, form_type, collection_id, group_id):  # pylint: disable=too-many-locals
    answer_store = get_answer_store(current_user)
    if _household_answers_changed(answer_store):
        _remove_repeating_on_household_answers(answer_store, group_id)

    error_messages = SchemaHelper.get_messages(g.schema_json)

    disable_mandatory = any(x in request.form for x in ['action[add_answer]', 'action[remove_answer]', 'action[save_sign_out]'])

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

    if _is_invalid_form(form) or 'action[add_answer]' in request.form or 'action[remove_answer]' in request.form:
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
def get_thank_you(eq_id, form_type, collection_id):  # pylint: disable=unused-argument
    survey_completed_metadata = current_app.eq['session_storage'].get_survey_completed_metadata()
    schema = load_schema_from_params(eq_id, form_type)

    if survey_completed_metadata:
        metadata_context = build_metadata_context_for_survey_completed(survey_completed_metadata)
        thank_you_template = render_theme_template(schema['theme'],
                                                   template_name='thank-you.html',
                                                   meta=metadata_context,
                                                   analytics_ua_id=current_app.config['EQ_UA_ID'],
                                                   survey_id=schema['survey_id'],
                                                   survey_title=TemplateRenderer.safe_content(schema['title']))
        return thank_you_template
    else:
        return _redirect_to_latest_location(collection_id, eq_id, form_type, schema)


@login_required
def _redirect_to_latest_location(collection_id, eq_id, form_type, schema):
    metadata = get_metadata(current_user)
    answer_store = get_answer_store(current_user)
    path_finder = PathFinder(schema, answer_store, metadata)
    routing_path = path_finder.get_routing_path()
    latest_location = path_finder.get_latest_location(get_completed_blocks(current_user),
                                                      routing_path=routing_path)
    return _redirect_to_location(collection_id, eq_id, form_type, latest_location)


@questionnaire_blueprint.route('signed-out', methods=["GET"])
def get_sign_out(eq_id, form_type, collection_id):  # pylint: disable=unused-argument
    schema = load_schema_from_params(eq_id, form_type)
    signed_out_template = render_theme_template(schema['theme'], template_name='signed-out.html',
                                                analytics_ua_id=current_app.config['EQ_UA_ID'],
                                                survey_title=TemplateRenderer.safe_content(schema['title']))
    return signed_out_template


@questionnaire_blueprint.route('timeout-continue', methods=["GET"])
@login_required
def get_timeout_continue(eq_id, form_type, collection_id):  # pylint: disable=unused-argument
    return 'true'


@questionnaire_blueprint.route('expire-session', methods=["POST"])
@login_required
def post_expire_session(eq_id, form_type, collection_id):  # pylint: disable=unused-argument
    _remove_survey_session_data()
    return get_session_expired(eq_id, form_type, collection_id)


@questionnaire_blueprint.route('session-expired', methods=["GET"])
def get_session_expired(eq_id, form_type, collection_id):  # pylint: disable=unused-argument
    schema = load_schema_from_params(eq_id, form_type)
    return render_theme_template(schema['theme'], template_name='session-expired.html',
                                 analytics_ua_id=current_app.config['EQ_UA_ID'],
                                 survey_title=TemplateRenderer.safe_content(schema['title']))


def submit_answers(eq_id, form_type, collection_id, metadata, answer_store):
    is_completed, invalid_location = is_survey_completed(answer_store, metadata)

    if is_completed:
        path_finder = PathFinder(g.schema_json, answer_store, metadata)

        message = convert_answers(metadata, g.schema_json, answer_store, path_finder.get_routing_path())
        message = current_app.eq['encrypter'].encrypt(message)
        sent = current_app.eq['submitter'].send_message(message,
                                                        current_app.config['EQ_RABBITMQ_QUEUE_NAME'],
                                                        metadata['tx_id'])

        if not sent:
            raise SubmissionFailedException()

        current_app.eq['session_storage'].store_survey_completed_metadata(metadata['tx_id'], metadata['period_str'], metadata['ru_ref'])
        get_questionnaire_store(current_user.user_id, current_user.user_ik).delete()
        _remove_survey_session_data()

        return redirect(url_for('.get_thank_you', eq_id=eq_id, form_type=form_type, collection_id=collection_id))
    else:
        return redirect(invalid_location.url(metadata))


@questionnaire_blueprint.route('<group_id>/<int:group_instance>/permanent-or-family-home', methods=["POST"])
@login_required
def post_everyone_at_address_confirmation(eq_id, form_type, collection_id, group_id, group_instance):
    if request.form.get('permanent-or-family-home-answer') == 'No':
        _remove_repeating_on_household_answers(get_answer_store(current_user), group_id)
    return post_block(eq_id, form_type, collection_id, group_id, group_instance, 'permanent-or-family-home')


def is_survey_completed(answer_store, metadata):
    path_finder = PathFinder(g.schema_json, answer_store, metadata)
    completed_blocks = get_completed_blocks(current_user)

    for location in path_finder.get_routing_path():
        if location.block_id in ['thank-you', 'summary', 'confirmation']:
            continue

        if location not in completed_blocks:
            return False, location

    return True, None


def _save_sign_out(collection_id, eq_id, form_type, this_location, form):
    questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)
    block_json = _render_schema(this_location)
    if _is_invalid_form(form):
        content = {'block': block_json, 'form': form}
        return _build_template(this_location, content, template=block_json['type'])
    else:
        _update_questionnaire_store(this_location, form)
        if this_location in questionnaire_store.completed_blocks:
            questionnaire_store.completed_blocks.remove(this_location)
            questionnaire_store.add_or_update()

        _remove_survey_session_data()
        return redirect(url_for('.get_sign_out', eq_id=eq_id, form_type=form_type, collection_id=collection_id))


def _remove_survey_session_data():
    current_app.eq['session_storage'].delete_session_from_db()
    current_app.eq['session_storage'].remove_user_ik()
    logout_user()


def _household_answers_changed(answer_store):
    household_answers = answer_store.filter(block_id="household-composition")
    stripped_form = request.form.copy()
    del stripped_form['csrf_token']
    remove = [k for k in stripped_form if 'action[' in k]
    for k in remove:
        del stripped_form[k]
    if len(household_answers) != len(stripped_form):
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
                if answer_value_empty(answer_value):
                    _remove_answer_from_questionnaire_store(answer_id, location, questionnaire_store)
                else:
                    formatted_answer_value = _format_answer_value(answer_value)
                    if formatted_answer_value:
                        answer = Answer(answer_id=answer_id, value=formatted_answer_value, location=location)
            elif answer_value is not None:
                answer = Answer(answer_id=answer_id, value=answer_value, location=location)
            else:
                _remove_answer_from_questionnaire_store(answer_id, location, questionnaire_store)

            if answer:
                questionnaire_store.answer_store.add_or_update(answer)

    if location not in questionnaire_store.completed_blocks:
        questionnaire_store.completed_blocks.append(location)


def _remove_answer_from_questionnaire_store(answer_id, location, questionnaire_store):
    questionnaire_store.answer_store.remove(location=location, answer_id=answer_id, answer_instance=0)


def answer_value_empty(answer_value_dict):
    return all(not value for value in answer_value_dict.values())


def _format_answer_value(answer_value):
    formatted_answer_value = None
    is_day_month_year = 'day' in answer_value and 'month' in answer_value and 'year' in answer_value
    is_month_year = 'day' not in answer_value and 'year' in answer_value and 'month' in answer_value

    if is_day_month_year and answer_value['day'] and answer_value['month']:
        formatted_answer_value = "{:02d}/{:02d}/{}".format(
            int(answer_value['day']),
            int(answer_value['month']),
            answer_value['year'],
        )
    elif is_month_year and answer_value['month']:
        formatted_answer_value = "{:02d}/{}".format(int(answer_value['month']), answer_value['year'])
    return formatted_answer_value


def update_questionnaire_store_with_answer_data(questionnaire_store, location, answers):

    survey_answer_ids = SchemaHelper.get_answer_ids_for_location(g.schema_json, location)

    for answer in [a for a in answers if a.answer_id in survey_answer_ids]:
        questionnaire_store.answer_store.add_or_update(answer)

    if location not in questionnaire_store.completed_blocks:
        questionnaire_store.completed_blocks.append(location)


def _is_invalid_form(form):
    is_valid = form.validate()
    if form.csrf_token.errors:
        logger.warn('Invalid csrf token')
        raise Forbidden

    return not is_valid


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


def _redirect_to_location(collection_id, eq_id, form_type, location):
    return redirect(url_for('.get_block', eq_id=eq_id, form_type=form_type, collection_id=collection_id,
                            group_id=location.group_id,
                            group_instance=location.group_instance, block_id=location.block_id))


def _get_context(block, current_location, answer_store):

    error_messages = SchemaHelper.get_messages(g.schema_json)
    form, template_params = get_form_for_location(block, current_location, answer_store, error_messages)
    content = {'form': form, 'block': block}
    if template_params:
        content.update(template_params)

    if block['type'] == 'Summary':
        metadata = get_metadata(current_user)
        aliases = SchemaHelper.get_aliases(g.schema_json)
        schema_context = build_schema_context(metadata, aliases, answer_store)
        rendered_schema_json = renderer.render(g.schema_json, **schema_context)
        content.update({'summary': build_summary_rendering_context(rendered_schema_json, answer_store, metadata)})

    return content


def _render_schema(current_location):
    metadata = get_metadata(current_user)
    answer_store = get_answer_store(current_user)
    block_json = SchemaHelper.get_block_for_location(g.schema_json, current_location)
    block_json = _evaluate_skip_conditions(block_json, current_location, answer_store, metadata)
    aliases = SchemaHelper.get_aliases(g.schema_json)
    block_context = build_schema_context(metadata, aliases, answer_store, current_location.group_instance)
    return renderer.render(block_json, **block_context)


def _get_front_end_navigation(answer_store, current_location, metadata, routing_path=None):
    completed_blocks = get_completed_blocks(current_user)
    navigation = Navigation(g.schema_json, answer_store, metadata, completed_blocks, routing_path)
    block_json = SchemaHelper.get_block_for_location(g.schema_json, current_location)
    if block_json is not None and block_json['type'] in ('Questionnaire', 'Interstitial', 'Confirmation', 'Summary'):
        return navigation.build_navigation(current_location.group_id, current_location.group_instance)
    else:
        return None


def get_page_title_for_location(schema_json, current_location):
    block = SchemaHelper.get_block_for_location(schema_json, current_location)
    if block['type'] == 'Interstitial':
        group = SchemaHelper.get_group(schema_json, current_location.group_id)
        page_title = '{group_title} - {survey_title}'.format(group_title=group['title'], survey_title=schema_json['title'])
    elif block['type'] == 'Questionnaire':
        first_question = next(SchemaHelper.get_questions_for_block(block))
        page_title = '{question_title} - {survey_title}'.format(question_title=first_question['title'], survey_title=schema_json['title'])
    else:
        page_title = schema_json['title']

    return TemplateRenderer.safe_content(page_title)


def _build_template(current_location, context, template, routing_path=None):
    metadata = get_metadata(current_user)
    metadata_context = build_metadata_context(metadata)

    answer_store = get_answer_store(current_user)
    front_end_navigation = _get_front_end_navigation(answer_store, current_location, metadata, routing_path)

    path_finder = PathFinder(g.schema_json, answer_store, metadata)
    previous_location = path_finder.get_previous_location(current_location)

    previous_url = previous_location.url(metadata) if previous_location is not None else None
    return _render_template(context, current_location, template, front_end_navigation, metadata_context, previous_url)


def _render_template(context, current_location, template, front_end_navigation, metadata_context, previous_url):
    theme = g.schema_json.get('theme', None)
    logger.debug("theme selected", theme=theme)
    session_timeout = current_app.config['EQ_SESSION_TIMEOUT_SECONDS']
    schema_session_timeout = g.schema_json.get('session_timeout_in_seconds')
    if schema_session_timeout is not None and schema_session_timeout < current_app.config['EQ_SESSION_TIMEOUT_SECONDS']:
        session_timeout = schema_session_timeout
    session_timeout_prompt = g.schema_json.get('session_prompt_in_seconds') or current_app.config['EQ_SESSION_TIMEOUT_PROMPT_SECONDS']

    survey_data = metadata_context['survey']
    url_prefix = '/questionnaire/{}/{}/{}'.format(survey_data['eq_id'], survey_data['form_type'], survey_data['collection_id'])

    page_title = get_page_title_for_location(g.schema_json, current_location)
    template = '{}.html'.format(template).lower()
    return render_theme_template(theme, template,
                                 meta=metadata_context,
                                 content=context,
                                 current_location=current_location,
                                 analytics_ua_id=current_app.config['EQ_UA_ID'],
                                 previous_location=previous_url,
                                 navigation=front_end_navigation,
                                 survey_title=TemplateRenderer.safe_content(g.schema_json['title']),
                                 legal_basis=g.schema_json['legal_basis'],
                                 survey_id=g.schema_json['survey_id'],
                                 session_timeout=session_timeout,
                                 session_timeout_prompt=session_timeout_prompt,
                                 url_prefix=url_prefix,
                                 page_title=page_title)

import re
from collections import defaultdict

from flask import Blueprint, g, redirect, request, url_for, current_app
from flask_login import current_user, login_required
from flask_themes2 import render_theme_template
from sdc.crypto.encrypter import encrypt

from structlog import get_logger

from app.data_model.answer_store import Answer
from app.globals import get_answer_store, get_completed_blocks, get_metadata, get_questionnaire_store
from app.helpers.form_helper import get_form_for_location, post_form_for_location
from app.helpers.schema_helper import SchemaHelper
from app.helpers.path_finder_helper import path_finder, full_routing_path_required
from app.helpers.session_helper import remove_survey_session_data
from app.helpers import template_helper
from app.questionnaire.location import Location
from app.questionnaire.navigation import Navigation

from app.questionnaire.rules import evaluate_skip_conditions
from app.keys import KEY_PURPOSE_SUBMISSION
from app.submitter.converter import convert_answers
from app.submitter.submission_failed import SubmissionFailedException
from app.templating.metadata_context import build_metadata_context_for_survey_completed
from app.templating.schema_context import build_schema_context
from app.templating.summary_context import build_summary_rendering_context
from app.templating.template_renderer import renderer, TemplateRenderer

from app.utilities.schema import load_schema_from_metadata, load_schema_from_params
from app.views.errors import MultipleSurveyError

END_BLOCKS = 'Summary', 'Confirmation'

logger = get_logger()

questionnaire_blueprint = Blueprint(name='questionnaire',
                                    import_name=__name__,
                                    url_prefix='/questionnaire/<eq_id>/<form_type>/<collection_id>/')


@questionnaire_blueprint.before_request
def before_request():
    metadata = get_metadata(current_user)
    if metadata:
        logger.bind(tx_id=metadata['tx_id'])

    values = request.view_args
    logger.bind(eq_id=values['eq_id'], form_type=values['form_type'],
                ce_id=values['collection_id'])
    logger.info('questionnaire request', method=request.method, url_path=request.full_path)

    if metadata:
        g.schema_json = load_schema_from_metadata(metadata)
        _check_same_survey(values['eq_id'], values['form_type'], values['collection_id'])


@questionnaire_blueprint.after_request
def add_cache_control(response):
    response.cache_control.no_cache = True

    return response


def save_questionnaire_store(func):
    def save_questionnaire_store_wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        if not current_user.is_anonymous:
            questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)

            questionnaire_store.add_or_update()

        return response

    return save_questionnaire_store_wrapper


@questionnaire_blueprint.route('<group_id>/<int:group_instance>/<block_id>', methods=['GET'])
@login_required
@full_routing_path_required
def get_block(routing_path, eq_id, form_type, collection_id, group_id, group_instance, block_id):  # pylint: disable=unused-argument,too-many-locals
    current_location = Location(group_id, group_instance, block_id)

    if not _is_valid_group(group_id) or not _is_valid_location(current_location):
        return _redirect_to_latest_location(routing_path, collection_id, eq_id, form_type)

    block = _render_schema(routing_path, current_location)

    if _is_skipping_to_the_end(routing_path, block, current_location):
        return _redirect_to_latest_location(routing_path, collection_id, eq_id, form_type)

    return _render_block(routing_path, block, current_location)


@questionnaire_blueprint.route('<group_id>/<int:group_instance>/<block_id>', methods=['POST'])
@login_required
@full_routing_path_required
def post_block(routing_path, eq_id, form_type, collection_id, group_id, group_instance, block_id):  # pylint: disable=too-many-locals
    current_location = Location(group_id, group_instance, block_id)

    if not _is_valid_group(group_id) or not _is_valid_location(current_location):
        return _redirect_to_latest_location(routing_path, collection_id, eq_id, form_type)

    block = _render_schema(routing_path, current_location)
    form = _generate_wtf_form(request.form, block, current_location)

    if 'action[save_sign_out]' in request.form:
        return _save_sign_out(routing_path, current_location, form)

    if form.validate():
        _update_questionnaire_store(current_location, form)
        next_location = path_finder.get_next_location(current_location=current_location)

        if _is_end_of_questionnaire(block, next_location):
            return submit_answers(routing_path, eq_id, form_type, collection_id)

        return redirect(_next_location_url(next_location))

    return _render_block(routing_path, block, current_location, post_form=form)


@questionnaire_blueprint.route('<group_id>/0/household-composition', methods=['POST'])
@login_required
@full_routing_path_required
def post_household_composition(routing_path, **kwargs):
    group_id = kwargs['group_id']
    answer_store = get_answer_store(current_user)
    if _household_answers_changed(answer_store):
        _remove_repeating_on_household_answers(answer_store, group_id)

    error_messages = SchemaHelper.get_messages(g.schema_json)

    disable_mandatory = any(x in request.form for x in ['action[add_answer]', 'action[remove_answer]', 'action[save_sign_out]'])

    current_location = Location(group_id, 0, 'household-composition')
    block = _render_schema(routing_path, current_location)
    form, _ = post_form_for_location(block, current_location, answer_store, request.form, error_messages, disable_mandatory=disable_mandatory)

    if 'action[add_answer]' in request.form:
        form.household.append_entry()

        return _render_block(routing_path, block, current_location, post_form=form)

    if 'action[remove_answer]' in request.form:
        index_to_remove = int(request.form.get('action[remove_answer]'))
        form.remove_person(index_to_remove)

        return _render_block(routing_path, block, current_location, post_form=form)

    if 'action[save_sign_out]' in request.form:
        response = _save_sign_out(routing_path, current_location, form)
        remove_empty_household_members_from_answer_store(answer_store, group_id)

        return response

    if form.validate():
        questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)
        update_questionnaire_store_with_answer_data(questionnaire_store, current_location, form.serialise(current_location))

        metadata = get_metadata(current_user)
        next_location = path_finder.get_next_location(current_location=current_location)

        return redirect(next_location.url(metadata))

    return _render_block(routing_path, block, current_location, form)


@questionnaire_blueprint.route('thank-you', methods=['GET'])
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

    routing_path = path_finder.get_full_routing_path()
    return _redirect_to_latest_location(routing_path, collection_id, eq_id, form_type)


def _redirect_to_latest_location(routing_path, collection_id, eq_id, form_type):
    latest_location = path_finder.get_latest_location(get_completed_blocks(current_user),
                                                      routing_path=routing_path)
    return _redirect_to_location(collection_id, eq_id, form_type, latest_location)


@questionnaire_blueprint.route('<group_id>/<int:group_instance>/permanent-or-family-home', methods=['POST'])
@login_required
def post_everyone_at_address_confirmation(eq_id, form_type, collection_id, group_id, group_instance):
    if request.form.get('permanent-or-family-home-answer') == 'No':
        _remove_repeating_on_household_answers(get_answer_store(current_user), group_id)
    return post_block(eq_id, form_type, collection_id, group_id, group_instance, 'permanent-or-family-home')  # pylint: disable=no-value-for-parameter


def _render_block(full_routing_path, block, current_location, post_form=None):

    if post_form is None:
        context = _get_context(full_routing_path, block, current_location, get_answer_store(current_user))
    else:
        context = {'form': post_form, 'block': block}

    return _build_template(
        current_location,
        context,
        block['type'],
        routing_path=full_routing_path)


def _is_valid_location(location):
    return location in path_finder.get_routing_path(
        location.group_id,
        location.group_instance,
    )


def _is_valid_group(group_id):
    return group_id in SchemaHelper.get_group_ids(g.schema_json)


def _generate_wtf_form(form, block, location):
    error_messages = SchemaHelper.get_messages(g.schema_json)
    disable_mandatory = 'action[save_sign_out]' in form

    wtf_form, _ = post_form_for_location(
        block,
        location,
        get_answer_store(current_user),
        request.form,
        error_messages,
        disable_mandatory)

    return wtf_form


def _next_location_url(location):
    metadata = get_metadata(current_user)
    return location.url(metadata)


def _is_end_of_questionnaire(block, next_location):

    return next_location is None and \
        block['type'] in END_BLOCKS


def _is_skipping_to_the_end(routing_path, block, current_location):
    latest_location = path_finder.get_latest_location(
        get_completed_blocks(current_user),
        routing_path=routing_path,
    )

    return current_location != latest_location and \
        block['type'] in END_BLOCKS


def submit_answers(routing_path, eq_id, form_type, collection_id):
    is_completed, invalid_location = is_survey_completed(routing_path)
    metadata = get_metadata(current_user)
    answer_store = get_answer_store(current_user)

    if is_completed:
        message = convert_answers(
            metadata,
            g.schema_json,
            answer_store,
            routing_path,
        )

        encrypted_message = encrypt(message, current_app.eq['key_store'], KEY_PURPOSE_SUBMISSION)
        sent = current_app.eq['submitter'].send_message(
            encrypted_message,
            current_app.config['EQ_RABBITMQ_QUEUE_NAME'],
            metadata['tx_id'],
        )

        if not sent:
            raise SubmissionFailedException()

        current_app.eq['session_storage'].store_survey_completed_metadata(
            metadata['tx_id'],
            metadata['period_str'],
            metadata['ru_ref'])

        get_questionnaire_store(current_user.user_id, current_user.user_ik).delete()
        remove_survey_session_data()

        return redirect(url_for(
            '.get_thank_you',
            eq_id=eq_id,
            form_type=form_type,
            collection_id=collection_id))
    else:
        return redirect(invalid_location.url(metadata))


def is_survey_completed(full_routing_path):
    completed_blocks = get_completed_blocks(current_user)

    for location in full_routing_path:
        if location.block_id in ['thank-you', 'summary', 'confirmation']:
            continue

        if location not in completed_blocks:
            return False, location

    return True, None


def _save_sign_out(routing_path, this_location, form):
    questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)
    block = _render_schema(routing_path, this_location)
    if form.validate():
        _update_questionnaire_store(this_location, form)

        if this_location in questionnaire_store.completed_blocks:
            questionnaire_store.completed_blocks.remove(this_location)
            questionnaire_store.add_or_update()

        remove_survey_session_data()

        return redirect(url_for('session.get_sign_out'))

    return _render_block(routing_path, block, this_location, post_form=form)


def _household_answers_changed(answer_store):
    household_answers = answer_store.filter(block_id='household-composition')
    stripped_form = request.form.copy()
    del stripped_form['csrf_token']
    remove = [k for k in stripped_form if 'action[' in k]
    for k in remove:
        del stripped_form[k]
    if len(household_answers) != len(stripped_form):
        return True
    for answer in request.form:
        answer_id, answer_index = extract_answer_id_and_instance(answer)

        stored_answer = next(
            (d for d in household_answers if d['answer_id'] == answer_id and
             d['answer_instance'] == answer_index),
            None,
        )

        if stored_answer and (stored_answer['value'] or '') != request.form[answer]:
            return True

    return False


def _remove_repeating_on_household_answers(answer_store, group_id):
    answer_store.remove(group_id=group_id, block_id='household-composition')
    questionnaire_store = get_questionnaire_store(
        current_user.user_id,
        current_user.user_ik,
    )

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


@save_questionnaire_store
def update_questionnaire_store_with_form_data(questionnaire_store, location, answer_dict):

    survey_answer_ids = SchemaHelper.get_answer_ids_for_location(g.schema_json, location)

    for answer_id, answer_value in answer_dict.items():
        if answer_id in survey_answer_ids or location.block_id == 'household-composition':
            answer = None

            # Dates are comprised of 3 string values
            if isinstance(answer_value, dict):
                if answer_value_empty(answer_value):
                    _remove_answer_from_questionnaire_store(answer_id, questionnaire_store)
                else:
                    formatted_answer_value = _format_answer_value(answer_value)
                    if formatted_answer_value:
                        answer = Answer(answer_id=answer_id, value=formatted_answer_value, location=location)
            elif answer_value is not None:
                answer = Answer(answer_id=answer_id, value=answer_value, location=location)
            else:
                _remove_answer_from_questionnaire_store(answer_id, questionnaire_store)

            if answer:
                questionnaire_store.answer_store.add_or_update(answer)

    if location not in questionnaire_store.completed_blocks:
        questionnaire_store.completed_blocks.append(location)


def _remove_answer_from_questionnaire_store(answer_id, questionnaire_store):
    questionnaire_store.answer_store.remove(answer_id=answer_id, answer_instance=0)


def answer_value_empty(answer_value_dict):
    return all(not value for value in answer_value_dict.values())


def _format_answer_value(answer_value):
    formatted_answer_value = None
    is_day_month_year = 'day' in answer_value and 'month' in answer_value and 'year' in answer_value
    is_month_year = 'day' not in answer_value and 'year' in answer_value and 'month' in answer_value

    if is_day_month_year and answer_value['day'] and answer_value['month']:
        formatted_answer_value = '{:02d}/{:02d}/{}'.format(
            int(answer_value['day']),
            int(answer_value['month']),
            answer_value['year'],
        )
    elif is_month_year and answer_value['month']:
        formatted_answer_value = '{:02d}/{}'.format(int(answer_value['month']), answer_value['year'])
    return formatted_answer_value


@save_questionnaire_store
def update_questionnaire_store_with_answer_data(questionnaire_store, location, answers):

    survey_answer_ids = SchemaHelper.get_answer_ids_for_location(g.schema_json, location)

    for answer in [a for a in answers if a.answer_id in survey_answer_ids]:
        questionnaire_store.answer_store.add_or_update(answer)

    if location not in questionnaire_store.completed_blocks:
        questionnaire_store.completed_blocks.append(location)


def _check_same_survey(eq_id, form_type, collection_id):
    metadata = get_metadata(current_user)
    current_survey = eq_id + form_type + collection_id
    metadata_survey = metadata['eq_id'] + metadata['form_type'] + metadata['collection_exercise_sid']
    if current_survey != metadata_survey:
        raise MultipleSurveyError


def _evaluate_skip_conditions(block_json, location, answer_store, metadata):
    for question in SchemaHelper.get_questions_for_block(block_json):
        if 'skip_conditions' in question:
            skip_question = evaluate_skip_conditions(question['skip_conditions'], metadata, answer_store, location.group_instance)
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


def _get_context(full_routing_path, block, current_location, answer_store):

    error_messages = SchemaHelper.get_messages(g.schema_json)
    form, template_params = get_form_for_location(block, current_location, answer_store, error_messages)

    content = {'form': form, 'block': block}
    if template_params:
        content.update(template_params)

    if block['type'] == 'Summary':
        metadata = get_metadata(current_user)
        aliases = SchemaHelper.get_aliases(g.schema_json)
        schema_context = build_schema_context(metadata=metadata,
                                              aliases=aliases,
                                              answer_store=answer_store,
                                              routing_path=full_routing_path)
        rendered_schema_json = renderer.render(g.schema_json, **schema_context)
        content.update({'summary': build_summary_rendering_context(rendered_schema_json, answer_store, metadata)})

    return content


def _render_schema(full_routing_path, current_location):
    metadata = get_metadata(current_user)
    answer_store = get_answer_store(current_user)
    block_json = SchemaHelper.get_block_for_location(g.schema_json, current_location)
    block_json = _evaluate_skip_conditions(block_json, current_location, answer_store, metadata)
    aliases = SchemaHelper.get_aliases(g.schema_json)
    block_context = build_schema_context(metadata=metadata,
                                         aliases=aliases,
                                         answer_store=answer_store,
                                         group_instance=current_location.group_instance,
                                         routing_path=full_routing_path)
    return renderer.render(block_json, **block_context)


def _get_front_end_navigation(answer_store, current_location, metadata, routing_path=None):
    completed_blocks = get_completed_blocks(current_user)
    navigation = Navigation(g.schema_json, answer_store, metadata, completed_blocks, routing_path)
    block_json = SchemaHelper.get_block_for_location(g.schema_json, current_location)
    if block_json is not None and block_json['type'] in ('Questionnaire', 'Interstitial', 'Confirmation', 'Summary'):
        return navigation.build_navigation(current_location.group_id, current_location.group_instance)

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
    answer_store = get_answer_store(current_user)
    front_end_navigation = _get_front_end_navigation(answer_store, current_location, metadata, routing_path)
    previous_location = path_finder.get_previous_location(current_location)
    previous_url = previous_location.url(metadata) if previous_location is not None else None

    return _render_template(context, current_location, template, front_end_navigation, previous_url)


@template_helper.with_session_timeout
@template_helper.with_questionnaire_url_prefix
@template_helper.with_metadata
@template_helper.with_analytics
@template_helper.with_legal_basis
def _render_template(context, current_location, template, front_end_navigation, previous_url, **kwargs):
    page_title = get_page_title_for_location(g.schema_json, current_location)

    return template_helper.render_template(
        template,
        content=context,
        current_location=current_location,
        navigation=front_end_navigation,
        previous_location=previous_url,
        page_title=page_title,
        **kwargs
    )

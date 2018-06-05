import re
from collections import defaultdict
from datetime import datetime, timedelta
import simplejson as json
import humanize as humanize

from flask import Blueprint, g, redirect, request, url_for, current_app, jsonify
from flask_login import current_user, login_required, logout_user
from flask_themes2 import render_theme_template
from sdc.crypto.encrypter import encrypt

from structlog import get_logger

from app.globals import get_session_store, is_dynamodb_enabled, get_completeness
from app.data_model.answer_store import Answer, AnswerStore
from app.data_model import submitted_responses
from app.globals import get_answer_store, get_completed_blocks, get_metadata, get_questionnaire_store
from app.helpers.form_helper import post_form_for_location
from app.helpers.path_finder_helper import path_finder, full_routing_path_required
from app.helpers import template_helper

from app.questionnaire.location import Location
from app.questionnaire.navigation import Navigation
from app.questionnaire.path_finder import PathFinder
from app.questionnaire.rules import get_answer_ids_on_routing_path

from app.questionnaire.rules import evaluate_skip_conditions
from app.keys import KEY_PURPOSE_SUBMISSION
from app.storage.storage_encryption import StorageEncryption
from app.submitter.converter import convert_answers
from app.submitter.submission_failed import SubmissionFailedException
from app.templating.metadata_context import build_metadata_context_for_survey_completed
from app.templating.schema_context import build_schema_context
from app.templating.summary_context import build_summary_rendering_context
from app.templating.template_renderer import renderer, TemplateRenderer
from app.templating.view_context import build_view_context

from app.utilities.schema import load_schema_from_metadata, load_schema_from_session_data
from app.views.errors import MultipleSurveyError
from app.authentication.no_token_exception import NoTokenException

END_BLOCKS = 'Summary', 'Confirmation'

logger = get_logger()

questionnaire_blueprint = Blueprint(name='questionnaire',
                                    import_name=__name__,
                                    url_prefix='/questionnaire/<eq_id>/<form_type>/<collection_id>/')

post_submission_blueprint = Blueprint(name='post_submission',
                                      import_name=__name__,
                                      url_prefix='/questionnaire/<eq_id>/<form_type>/')


@questionnaire_blueprint.before_request
def before_questionnaire_request():
    metadata = get_metadata(current_user)
    if not metadata:
        raise NoTokenException(401)

    logger.bind(tx_id=metadata['tx_id'])

    values = request.view_args
    logger.bind(eq_id=values['eq_id'], form_type=values['form_type'],
                ce_id=values['collection_id'])
    logger.info('questionnaire request', method=request.method, url_path=request.full_path)

    _check_same_survey(url_eq_id=values['eq_id'],
                       url_form_type=values['form_type'],
                       url_collection_id=values['collection_id'],
                       session_eq_id=metadata['eq_id'],
                       session_form_type=metadata['form_type'],
                       session_collection_id=metadata['collection_exercise_sid'])

    g.schema = load_schema_from_metadata(metadata)


@post_submission_blueprint.before_request
def before_post_submission_request():
    session = get_session_store()
    if not session or not session.session_data:
        raise NoTokenException(401)

    session_data = session.session_data

    logger.bind(tx_id=session_data.tx_id)

    values = request.view_args
    logger.bind(eq_id=values['eq_id'], form_type=values['form_type'])
    logger.info('questionnaire request', method=request.method, url_path=request.full_path)

    _check_same_survey(url_eq_id=values['eq_id'],
                       url_form_type=values['form_type'],
                       url_collection_id='',
                       session_eq_id=session_data.eq_id,
                       session_form_type=session_data.form_type,
                       session_collection_id='')


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

    if not _is_valid_location(routing_path, current_location):
        return _redirect_to_latest_location(collection_id, eq_id, form_type)

    block = _get_block_json(current_location)

    if _is_skipping_to_the_end(block, current_location):
        return _redirect_to_latest_location(collection_id, eq_id, form_type)

    context = _get_context(routing_path, block, current_location)
    return _render_page(block['type'], context, current_location, routing_path)


@questionnaire_blueprint.route('<group_id>/<int:group_instance>/<block_id>', methods=['POST'])
@login_required
@full_routing_path_required
def post_block(routing_path, eq_id, form_type, collection_id, group_id, group_instance, block_id):  # pylint: disable=too-many-locals
    current_location = Location(group_id, group_instance, block_id)
    metadata = get_metadata(current_user)
    answer_store = get_answer_store(current_user)

    if not _is_valid_location(routing_path, current_location):
        return _redirect_to_latest_location(collection_id, eq_id, form_type)

    block = _get_block_json(current_location)

    schema_context = _get_schema_context(routing_path, current_location.group_instance, metadata, answer_store)
    rendered_block = renderer.render(block, **schema_context)

    form = _generate_wtf_form(request.form, rendered_block, current_location)

    if 'action[save_sign_out]' in request.form:
        return _save_sign_out(routing_path, current_location, form)

    if form.validate():
        _update_questionnaire_store(current_location, form)
        next_location = path_finder.get_next_location(current_location=current_location)

        if _is_end_of_questionnaire(block, next_location):
            return submit_answers(routing_path, eq_id, form_type)

        return redirect(_next_location_url(next_location))

    context = build_view_context(block['type'], metadata, answer_store, schema_context, rendered_block, current_location, form)

    return _render_page(block['type'], context, current_location, routing_path)


@questionnaire_blueprint.route('<group_id>/0/household-composition', methods=['POST'])
@login_required
@full_routing_path_required
def post_household_composition(routing_path, **kwargs):
    group_id = kwargs['group_id']
    answer_store = get_answer_store(current_user)
    if _household_answers_changed(answer_store):
        _remove_repeating_on_household_answers(answer_store)

    disable_mandatory = any(x in request.form for x in ['action[add_answer]', 'action[remove_answer]', 'action[save_sign_out]'])

    current_location = Location(group_id, 0, 'household-composition')

    block = _get_block_json(current_location)

    form = post_form_for_location(g.schema, block, current_location, answer_store, get_metadata(current_user),
                                  request.form, disable_mandatory=disable_mandatory)

    form.validate()  # call validate here to keep errors in the form object on the context
    context = _get_context(routing_path, block, current_location, form)

    if 'action[add_answer]' in request.form:
        form.household.append_entry()

        return _render_page(block['type'], context, current_location, routing_path)

    if 'action[remove_answer]' in request.form:
        index_to_remove = int(request.form.get('action[remove_answer]'))
        form.remove_person(index_to_remove)

        return _render_page(block['type'], context, current_location, routing_path)

    if 'action[save_sign_out]' in request.form:
        response = _save_sign_out(routing_path, current_location, form)
        remove_empty_household_members_from_answer_store(answer_store)

        return response

    if form.validate():
        questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)
        update_questionnaire_store_with_answer_data(questionnaire_store, current_location, form.serialise())

        metadata = get_metadata(current_user)
        next_location = path_finder.get_next_location(current_location=current_location)

        return redirect(next_location.url(metadata))

    return _render_page(block['type'], context, current_location, routing_path)


@post_submission_blueprint.route('thank-you', methods=['GET'])
@login_required
def get_thank_you(eq_id, form_type):  # pylint: disable=unused-argument
    session_data = get_session_store().session_data

    if session_data.submitted_time:
        schema = load_schema_from_session_data(session_data)
        metadata_context = build_metadata_context_for_survey_completed(session_data)

        view_submission_url = None
        view_submission_duration = 0
        if _is_submission_viewable(schema.json, session_data.submitted_time):
            view_submission_url = url_for('.get_view_submission', eq_id=eq_id, form_type=form_type)
            view_submission_duration = humanize.naturaldelta(timedelta(seconds=schema.json['view_submitted_response']['duration']))

        return render_theme_template(schema.json['theme'],
                                     template_name='thank-you.html',
                                     metadata=metadata_context,
                                     analytics_ua_id=current_app.config['EQ_UA_ID'],
                                     survey_id=schema.json['survey_id'],
                                     survey_title=TemplateRenderer.safe_content(schema.json['title']),
                                     is_view_submitted_response_enabled=is_view_submitted_response_enabled(schema.json),
                                     view_submission_url=view_submission_url,
                                     view_submission_duration=view_submission_duration)

    metadata = get_metadata(current_user)
    g.schema = load_schema_from_metadata(metadata)
    collection_id = metadata['collection_exercise_sid']
    return _redirect_to_latest_location(collection_id, metadata.get('eq_id'), metadata.get('form_type'))


@post_submission_blueprint.route('view-submission', methods=['GET'])
@login_required
def get_view_submission(eq_id, form_type):  # pylint: disable=unused-argument

    session_data = get_session_store().session_data
    g.schema = load_schema_from_session_data(session_data)

    if _is_submission_viewable(g.schema.json, session_data.submitted_time):
        submitted_data = submitted_responses.get_item(session_data.tx_id)

        if submitted_data:

            metadata_context = build_metadata_context_for_survey_completed(session_data)

            pepper = current_app.eq['secret_store'].get_secret_by_name('EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER')
            encrypter = StorageEncryption(current_user.user_id, current_user.user_ik, pepper)

            submitted_data = json.loads(encrypter.decrypt_data(submitted_data['data']))
            answer_store = AnswerStore(existing_answers=submitted_data.get('answers'))

            metadata = submitted_data.get('metadata')

            routing_path = PathFinder(g.schema, answer_store, metadata, []).get_full_routing_path()

            schema_context = _get_schema_context(routing_path, 0, metadata, answer_store)
            rendered_schema = renderer.render(g.schema.json, **schema_context)
            summary_rendered_context = build_summary_rendering_context(g.schema, rendered_schema['sections'], answer_store, metadata)

            context = {
                'summary': {
                    'groups': summary_rendered_context,
                    'answers_are_editable': False,
                    'is_view_submission_response_enabled': is_view_submitted_response_enabled(g.schema.json),
                },
                'variables': None
            }

            return render_theme_template(g.schema.json['theme'],
                                         template_name='view-submission.html',
                                         metadata=metadata_context,
                                         analytics_ua_id=current_app.config['EQ_UA_ID'],
                                         survey_id=g.schema.json['survey_id'],
                                         survey_title=TemplateRenderer.safe_content(g.schema.json['title']),
                                         content=context)

    return redirect(url_for('post_submission.get_thank_you', eq_id=eq_id, form_type=form_type))


def _redirect_to_latest_location(collection_id, eq_id, form_type):
    latest_location = get_completeness(current_user).get_latest_location()

    return _redirect_to_location(collection_id, eq_id, form_type, latest_location)


def _render_page(block_type, context, current_location, routing_path):
    if request_wants_json():
        return jsonify(context)

    return _build_template(
        current_location,
        context,
        block_type,
        routing_path=routing_path)


def _is_valid_location(routing_path, location):
    return location in routing_path


def _generate_wtf_form(form, block, location):
    disable_mandatory = 'action[save_sign_out]' in form

    wtf_form = post_form_for_location(
        g.schema,
        block,
        location,
        get_answer_store(current_user),
        get_metadata(current_user),
        request.form,
        disable_mandatory)

    return wtf_form


def _next_location_url(location):
    metadata = get_metadata(current_user)
    return location.url(metadata)


def _is_end_of_questionnaire(block, next_location):
    return (
        block['type'] in END_BLOCKS and
        next_location is None
    )


def _is_skipping_to_the_end(block, current_location):
    latest_location = get_completeness(current_user).get_first_incomplete_location_in_survey()

    return (
        latest_location and
        current_location != latest_location and
        block['type'] in END_BLOCKS
    )


def submit_answers(routing_path, eq_id, form_type):
    metadata = get_metadata(current_user)
    answer_store = get_answer_store(current_user)

    invalid_location = get_completeness(current_user).get_first_incomplete_location_in_survey()

    if invalid_location:
        return redirect(invalid_location.url(metadata))
    else:
        message = json.dumps(convert_answers(
            metadata,
            g.schema,
            answer_store,
            routing_path,
        ))

        encrypted_message = encrypt(message, current_app.eq['key_store'], KEY_PURPOSE_SUBMISSION)
        sent = current_app.eq['submitter'].send_message(
            encrypted_message,
            current_app.config['EQ_RABBITMQ_QUEUE_NAME'],
            metadata['tx_id'],
        )

        if not sent:
            raise SubmissionFailedException()

        submitted_time = datetime.utcnow()

        _store_submitted_time_in_session(submitted_time)

        if is_view_submitted_response_enabled(g.schema.json):
            _store_viewable_submission(answer_store.answers, metadata, submitted_time)

        get_questionnaire_store(current_user.user_id, current_user.user_ik).delete()

        return redirect(url_for('post_submission.get_thank_you', eq_id=eq_id, form_type=form_type))


def _store_submitted_time_in_session(submitted_time):
    session_store = get_session_store()
    session_data = session_store.session_data
    session_data.submitted_time = submitted_time.isoformat()
    session_store.save()


def _store_viewable_submission(answers, metadata, submitted_time):
    pepper = current_app.eq['secret_store'].get_secret_by_name('EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER')
    encrypter = StorageEncryption(current_user.user_id, current_user.user_ik, pepper)
    encrypted_data = encrypter.encrypt_data(
        {
            'answers': answers,
            'metadata': metadata
        }
    )

    valid_until = submitted_time + timedelta(seconds=g.schema.json['view_submitted_response']['duration'])

    item = {
        'tx_id': metadata['tx_id'],
        'data': encrypted_data,
        'valid_until': valid_until
    }

    submitted_responses.put_item(item)


def is_view_submitted_response_enabled(schema):
    if is_dynamodb_enabled():
        view_submitted_response = schema.get('view_submitted_response')
        if view_submitted_response:
            return view_submitted_response['enabled']

    return False


def _is_submission_viewable(schema, submitted_time):
    if is_view_submitted_response_enabled(schema) and submitted_time:
        submitted_time = datetime.strptime(submitted_time, '%Y-%m-%dT%H:%M:%S.%f')
        submission_valid_until = submitted_time + timedelta(seconds=schema['view_submitted_response']['duration'])
        return submission_valid_until > datetime.utcnow()

    return False


def _save_sign_out(routing_path, this_location, form):
    questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)

    block = _get_block_json(this_location)

    if form.validate():
        _update_questionnaire_store(this_location, form)

        if this_location in questionnaire_store.completed_blocks:
            questionnaire_store.completed_blocks.remove(this_location)
            questionnaire_store.add_or_update()

        logout_user()

        return redirect(url_for('session.get_sign_out'))

    context = _get_context(routing_path, block, this_location, form)
    return _render_page(block['type'], context, this_location, routing_path)


def _household_answers_changed(answer_store):
    answer_ids = g.schema.get_answer_ids_for_block('household-composition')
    household_answers = answer_store.filter(answer_ids)
    stripped_form = request.form.copy()
    del stripped_form['csrf_token']
    remove = [k for k in stripped_form if 'action[' in k]
    for k in remove:
        del stripped_form[k]
    if household_answers.count() != len(stripped_form):
        return True
    for answer in request.form:
        answer_id, answer_index = extract_answer_id_and_instance(answer)

        try:
            stored_answer = household_answers.filter(
                answer_ids=[answer_id],
                answer_instance=answer_index)[0]
        except IndexError:
            stored_answer = None

        if stored_answer and (stored_answer['value'] or '') != request.form[answer]:
            return True

    return False


def _remove_repeating_on_household_answers(answer_store):
    answer_ids = g.schema.get_answer_ids_for_block('household-composition')
    answer_store.remove(answer_ids=answer_ids)
    questionnaire_store = get_questionnaire_store(
        current_user.user_id,
        current_user.user_ik,
    )

    for answer in g.schema.get_answers_that_repeat_in_block('household-composition'):
        groups_to_delete = g.schema.get_groups_that_repeat_with_answer_id(answer['id'])
        for group in groups_to_delete:
            answer_ids = g.schema.get_answer_ids_for_group(group['id'])
            answer_store.remove(answer_ids=answer_ids)
            questionnaire_store.completed_blocks[:] = [b for b in questionnaire_store.completed_blocks if
                                                       b.group_id != group['id']]


def remove_empty_household_members_from_answer_store(answer_store):
    answer_ids = g.schema.get_answer_ids_for_block('household-composition')
    household_answers = answer_store.filter(answer_ids=answer_ids)
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
        answer_store.remove(answer_ids=answer_ids, answer_instance=instance_to_remove)


def _update_questionnaire_store(current_location, form):
    questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)
    if current_location.block_id in ['relationships', 'household-relationships']:
        update_questionnaire_store_with_answer_data(questionnaire_store, current_location,
                                                    form.serialise())
    else:
        update_questionnaire_store_with_form_data(questionnaire_store, current_location, form.data)


@save_questionnaire_store
def update_questionnaire_store_with_form_data(questionnaire_store, location, answer_dict):

    survey_answer_ids = g.schema.get_answer_ids_for_block(location.block_id)

    for answer_id, answer_value in answer_dict.items():

        # If answer is not answered then check for a schema specified default
        if answer_value is None:
            answer_value = g.schema.get_answer(answer_id).get('default')

        if answer_id in survey_answer_ids or location.block_id == 'household-composition':

            if isinstance(answer_value, dict):
                answer_value = _return_date_answer_value(answer_value)

            if answer_value is not None:
                answer = Answer(answer_id=answer_id,
                                value=answer_value,
                                group_instance=location.group_instance,
                                group_id=location.group_id,
                                block_id=location.block_id)

                latest_answer_store_hash = questionnaire_store.answer_store.get_hash()
                questionnaire_store.answer_store.add_or_update(answer)
                if latest_answer_store_hash != questionnaire_store.answer_store.get_hash():
                    _remove_dependent_answers_from_completed_blocks(answer_id, questionnaire_store)
            else:
                _remove_answer_from_questionnaire_store(
                    answer_id,
                    questionnaire_store,
                    group_instance=location.group_instance)

    if location not in questionnaire_store.completed_blocks:
        questionnaire_store.completed_blocks.append(location)


def _return_date_answer_value(answer_value):
    if not answer_value_empty(answer_value):
        # Dates are comprised of 3 string values
        formatted_answer_value = _format_answer_value(answer_value)
        if formatted_answer_value:
            return formatted_answer_value

    return None


def _remove_dependent_answers_from_completed_blocks(answer_id, questionnaire_store):
    """
    Gets a list of answers ids that are dependent on the answer_id passed in.
    Then for each dependent answer it will remove it's block from those completed.
    This will therefore force the respondent to revisit that block.
    The dependent answers themselves remain untouched.
    :param answer_id: the answer that has changed
    :param questionnaire_store: holds the completed blocks
    :return: None
    """
    dependencies = g.schema.get_answer_dependencies_by_id(answer_id)
    for dependency in dependencies:
        answer = g.schema.get_answer(dependency)
        question = g.schema.get_question(answer['parent_id'])
        block = g.schema.get_block(question['parent_id'])

        location = Location(block['parent_id'], 0, block['id'])
        if location in questionnaire_store.completed_blocks:
            questionnaire_store.completed_blocks.remove(location)


def _remove_answer_from_questionnaire_store(answer_id, questionnaire_store,
                                            group_instance=0):
    questionnaire_store.answer_store.remove(answer_ids=[answer_id],
                                            group_instance=group_instance,
                                            answer_instance=0)


def answer_value_empty(answer_value_dict):
    return all(not value for value in answer_value_dict.values())


def _format_answer_value(answer_value):
    formatted_answer_value = None
    is_day_month_year = 'day' in answer_value and 'month' in answer_value and 'year' in answer_value
    is_month_year = 'day' not in answer_value and 'year' in answer_value and 'month' in answer_value

    if is_day_month_year:
        formatted_answer_value = '{:04d}-{:02d}-{:02d}'.format(
            int(answer_value['year']),
            int(answer_value['month']),
            int(answer_value['day'])
        )
    elif is_month_year:
        formatted_answer_value = '{:04d}-{:02d}'.format(
            int(answer_value['year']),
            int(answer_value['month'])
        )
    return formatted_answer_value


@save_questionnaire_store
def update_questionnaire_store_with_answer_data(questionnaire_store, location, answers):

    survey_answer_ids = g.schema.get_answer_ids_for_block(location.block_id)

    for answer in [a for a in answers if a.answer_id in survey_answer_ids]:
        questionnaire_store.answer_store.add_or_update(answer)

    if location not in questionnaire_store.completed_blocks:
        questionnaire_store.completed_blocks.append(location)


def _check_same_survey(url_eq_id, url_form_type, url_collection_id, session_eq_id, session_form_type, session_collection_id):
    if url_eq_id != session_eq_id \
        or url_form_type != session_form_type \
            or url_collection_id != session_collection_id:
        raise MultipleSurveyError


def _evaluate_skip_conditions(block_json, location, answer_store, metadata):
    for question in g.schema.get_questions_for_block(block_json):
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
    return redirect(url_for('questionnaire.get_block', eq_id=eq_id, form_type=form_type, collection_id=collection_id,
                            group_id=location.group_id,
                            group_instance=location.group_instance, block_id=location.block_id))


def _get_context(full_routing_path, block, current_location, form=None):
    metadata = get_metadata(current_user)
    answer_store = get_answer_store(current_user)
    schema_context = _get_schema_context(full_routing_path, current_location.group_instance, metadata, answer_store)
    rendered_block = renderer.render(block, **schema_context)

    return build_view_context(block['type'], metadata, answer_store, schema_context, rendered_block, current_location, form=form)


def _get_block_json(current_location):
    metadata = get_metadata(current_user)
    answer_store = get_answer_store(current_user)
    block_json = g.schema.get_block(current_location.block_id)
    return _evaluate_skip_conditions(block_json, current_location, answer_store, metadata)


def _get_schema_context(full_routing_path, group_instance, metadata, answer_store):
    answer_ids_on_path = get_answer_ids_on_routing_path(g.schema, full_routing_path)

    return build_schema_context(metadata=metadata,
                                answer_store=answer_store,
                                group_instance=group_instance,
                                answer_ids_on_path=answer_ids_on_path)


def _get_front_end_navigation(answer_store, current_location, metadata, routing_path=None):
    completed_blocks = get_completed_blocks(current_user)
    navigation = Navigation(g.schema, answer_store, metadata, completed_blocks,
                            routing_path, get_completeness(current_user))
    block_json = g.schema.get_block(current_location.block_id)
    if block_json['type'] != 'Introduction':
        return navigation.build_navigation(current_location.group_id, current_location.group_instance)

    return None


def get_page_title_for_location(schema, current_location):
    block = schema.get_block(current_location.block_id)
    if block['type'] == 'Interstitial':
        group = schema.get_group(current_location.group_id)
        page_title = '{group_title} - {survey_title}'.format(group_title=group['title'], survey_title=schema.json['title'])
    elif block['type'] == 'Question':
        first_question = next(schema.get_questions_for_block(block))
        page_title = '{question_title} - {survey_title}'.format(question_title=first_question['title'], survey_title=schema.json['title'])
    else:
        page_title = schema.json['title']

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
    page_title = get_page_title_for_location(g.schema, current_location)

    return template_helper.render_template(
        template,
        content=context,
        current_location=current_location,
        navigation=front_end_navigation,
        previous_location=previous_url,
        page_title=page_title,
        **kwargs
    )


def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

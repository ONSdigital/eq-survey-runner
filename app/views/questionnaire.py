from datetime import datetime, timedelta

import flask_babel
import humanize
import simplejson as json
from dateutil.tz import tzutc
from flask import Blueprint, g, redirect, request, url_for, current_app, jsonify
from flask import session as cookie_session, render_template as flask_render_template
from flask_login import current_user, login_required, logout_user
from jwcrypto.common import base64url_decode
from sdc.crypto.encrypter import encrypt
from structlog import get_logger

from app.authentication.no_token_exception import NoTokenException
from app.data_model.answer_store import AnswerStore
from app.data_model.app_models import SubmittedResponse
from app.globals import (
    get_answer_store,
    get_completed_store,
    get_metadata,
    get_questionnaire_store,
    get_session_store,
)
from app.helpers.form_helper import post_form_for_block
from app.helpers.path_finder_helper import path_finder, section_routing_path_required
from app.helpers.schema_helpers import with_schema
from app.helpers.session_helpers import with_questionnaire_store
from app.helpers.template_helper import (
    with_session_timeout,
    with_analytics,
    with_legal_basis,
    render_template,
    safe_content,
)
from app.keys import KEY_PURPOSE_SUBMISSION
from app.questionnaire.questionnaire_store_updater import QuestionnaireStoreUpdater
from app.questionnaire.location import Location
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.questionnaire.router import Router
from app.questionnaire.schema_utils import transform_variants
from app.storage.storage_encryption import StorageEncryption
from app.submitter.converter import convert_answers
from app.submitter.submission_failed import SubmissionFailedException
from app.templating.metadata_context import build_metadata_context_for_survey_completed
from app.templating.summary_context import build_summary_rendering_context
from app.templating.view_context import build_view_context
from app.utilities.schema import load_schema_from_session_data
from app.views.exceptions import PageNotFoundException

END_BLOCKS = 'Summary', 'Confirmation'

logger = get_logger()

questionnaire_blueprint = Blueprint(
    name='questionnaire', import_name=__name__, url_prefix='/questionnaire/'
)

post_submission_blueprint = Blueprint(
    name='post_submission', import_name=__name__, url_prefix='/submitted/'
)


@questionnaire_blueprint.before_request
def before_questionnaire_request():
    metadata = get_metadata(current_user)
    if not metadata:
        raise NoTokenException(401)

    logger.bind(
        tx_id=metadata['tx_id'],
        schema_name=metadata['schema_name'],
        ce_id=metadata['collection_exercise_sid'],
        questionnaire_id=metadata['questionnaire_id'],
    )

    logger.info(
        'questionnaire request', method=request.method, url_path=request.full_path
    )

    session_store = get_session_store()
    session_data = session_store.session_data

    language_code = request.args.get('language_code')
    if language_code:
        session_data.language_code = language_code
        session_store.save()

    g.schema = load_schema_from_session_data(session_data)


@post_submission_blueprint.before_request
def before_post_submission_request():
    session_store = get_session_store()
    if not session_store or not session_store.session_data:
        raise NoTokenException(401)

    session_data = session_store.session_data
    g.schema = load_schema_from_session_data(session_data)

    logger.bind(tx_id=session_data.tx_id, schema_name=session_data.schema_name)

    logger.info(
        'questionnaire request', method=request.method, url_path=request.full_path
    )


@questionnaire_blueprint.route('/', methods=['GET'])
@login_required
@with_questionnaire_store
@with_schema
def get_questionnaire(schema, questionnaire_store):
    router = Router(schema, completed_store=questionnaire_store.completed_store)
    redirect_location = router.get_first_incomplete_location_in_survey()
    return redirect(redirect_location.url())


@questionnaire_blueprint.route('<block_id>/', methods=['GET'])
@questionnaire_blueprint.route('<list_name>/<block_id>/', methods=['GET'])
@questionnaire_blueprint.route(
    '<list_name>/<list_item_id>/<block_id>/', methods=['GET']
)
@login_required
@with_questionnaire_store
@with_schema
@section_routing_path_required
def get_block(
    routing_path,
    schema,
    questionnaire_store,
    block_id,
    list_name=None,
    list_item_id=None,
):
    return get_block_handler(
        routing_path, schema, questionnaire_store, block_id, list_name, list_item_id
    )


def validate_location(schema, routing_path, list_store, current_location):
    completed_store = get_completed_store(current_user)
    router = Router(schema, completed_store)

    if current_location.block_id not in [block['id'] for block in schema.get_blocks()]:
        redirect_location = router.get_first_incomplete_location_in_survey()
        return _redirect_to_location(redirect_location)

    is_list_collector_child = schema.is_block_list_collector_child(
        current_location.block_id
    )

    if is_list_collector_child:
        parent_block_id = schema.get_list_collector_for_block_id(
            current_location.block_id
        )['id']
        routing_location = Location(block_id=parent_block_id)
    else:
        routing_location = current_location

    if not router.can_access_location(routing_location, routing_path):
        redirect_location = router.get_first_incomplete_location_in_survey()
        return _redirect_to_location(redirect_location)

    if is_list_collector_child:
        list_item_id = current_location.list_item_id
        list_name = current_location.list_name
        block = schema.get_block(current_location.block_id)
        parent_block = schema.get_list_collector_for_block_id(current_location.block_id)

        if list_name != parent_block['populates_list']:
            logger.info(
                f'Mismatched list_name: {list_name} and block_id: {current_location.block_id}'
            )
            next_location = path_finder.get_first_incomplete_location(routing_path)
            return _redirect_to_location(next_location)

        if block['type'] == 'ListAddQuestion':
            if list_item_id:
                raise PageNotFoundException(
                    f'list_item_id included in route for add question on list collector'
                )
            return

        if list_item_id not in list_store[current_location.list_name]:
            return redirect(
                url_for('questionnaire.get_block', block_id=parent_block['id'])
            )


def get_block_handler(
    routing_path,
    schema,
    questionnaire_store,
    block_id,
    list_name=None,
    list_item_id=None,
):
    list_store = questionnaire_store.list_store
    metadata = questionnaire_store.metadata
    answer_store = questionnaire_store.answer_store
    current_location = Location(block_id, list_name, list_item_id)

    to_redirect = validate_location(schema, routing_path, list_store, current_location)
    if to_redirect:
        return to_redirect

    router = Router(schema, completed_store=questionnaire_store.completed_store)
    previous_location = router.get_previous_location(current_location, routing_path)

    return _render_block(
        schema, metadata, answer_store, block_id, current_location, previous_location
    )


# pylint: disable=too-many-locals
# pylint: disable=too-many-return-statements
def post_block_handler(
    routing_path,
    schema,
    questionnaire_store,  # noqa: C901
    block_id,
    list_name=None,
    list_item_id=None,
):

    metadata = questionnaire_store.metadata
    collection_metadata = questionnaire_store.collection_metadata
    list_store = questionnaire_store.list_store
    answer_store = questionnaire_store.answer_store

    current_location = Location(block_id, list_name, list_item_id)

    to_redirect = validate_location(schema, routing_path, list_store, current_location)
    if to_redirect:
        return to_redirect

    section = schema.get_section_for_block_id(block_id)
    block = schema.get_block(block_id)

    transformed_block = transform_variants(block, schema, metadata, answer_store)

    placeholder_renderer = PlaceholderRenderer(
        language=flask_babel.get_locale().language,
        answer_store=answer_store,
        metadata=metadata,
    )
    rendered_block = placeholder_renderer.render(transformed_block)

    form = _generate_wtf_form(request.form, rendered_block, schema)

    router = Router(schema, completed_store=questionnaire_store.completed_store)
    previous_location = router.get_previous_location(current_location, routing_path)

    if 'action[save_sign_out]' in request.form:
        return _save_sign_out(
            current_location, previous_location, rendered_block, form, schema
        )

    if 'action[sign_out]' in request.form:
        return redirect(url_for('session.get_sign_out'))

    if not form.validate():
        context = build_view_context(
            block['type'],
            metadata,
            schema,
            list_store,
            answer_store,
            rendered_block,
            current_location,
            form,
        )
        return _render_page(
            block['type'], context, current_location, previous_location, schema
        )

    _set_started_at_metadata_if_required(form, collection_metadata)
    questionnaire_store_updater = QuestionnaireStoreUpdater(
        current_location, schema, questionnaire_store, rendered_block.get('question')
    )

    list_collection_block = block['type'] in [
        'ListCollector',
        'ListAddQuestion',
        'ListEditQuestion',
        'ListRemoveQuestion',
    ]

    if list_collection_block:
        next_url = perform_list_action(
            schema,
            metadata,
            answer_store,
            current_location,
            form,
            rendered_block,
            questionnaire_store_updater,
            list_item_id,
        )
        if next_url:
            return redirect(next_url)

    if _is_end_of_questionnaire(block):
        return submit_answers(schema)

    questionnaire_store_updater.update_answers(form)
    questionnaire_store_updater.add_completed_location()

    # recreate routing path if the answers have changed
    if answer_store.is_dirty:
        routing_path = path_finder.routing_path(section)

    current_section_id = schema.get_section_for_block_id(block_id)['id']
    if path_finder.is_path_complete(routing_path):
        questionnaire_store_updater.add_completed_section(current_section_id)
    else:
        questionnaire_store_updater.remove_completed_section(current_section_id)

    questionnaire_store_updater.save()

    next_location = router.get_next_location(current_location, routing_path)

    return redirect(next_location.url())


def perform_list_action(
    schema,
    metadata,
    answer_store,
    current_location,
    form,
    rendered_block,
    questionnaire_store_updater,
    list_item_id,
):
    block = schema.get_block(current_location.block_id)

    parent_block = schema.get_list_collector_for_block_id(current_location.block_id)

    if block['type'] == 'ListCollector':
        if form.data[block['add_answer']['id']] == block['add_answer']['value']:
            questionnaire_store_updater.update_answers(form)
            questionnaire_store_updater.save()
            add_url = url_for(
                'questionnaire.get_block',
                list_name=rendered_block['populates_list'],
                block_id=rendered_block['add_block']['id'],
            )
            return add_url
        return

    if block['type'] == 'ListRemoveQuestion':
        if (
            form.data[parent_block['remove_answer']['id']]
            == parent_block['remove_answer']['value']
        ):
            list_name = parent_block['populates_list']
            questionnaire_store_updater.remove_list_item_and_answers(
                list_name, list_item_id
            )
        else:
            return url_for('questionnaire.get_block', block_id=parent_block['id'])

    if block['type'] == 'ListAddQuestion':
        questionnaire_store_updater.add_list_item_and_answers(
            form, parent_block['populates_list']
        )
    elif block['type'] == 'ListEditQuestion':
        questionnaire_store_updater.update_answers(form)

    # Clear the answer from the confirmation question on the list collector question
    transformed_parent = transform_variants(
        parent_block, schema, metadata, answer_store
    )
    answer_ids_to_remove = [
        answer['id'] for answer in transformed_parent['question']['answers']
    ]
    questionnaire_store_updater.remove_answers(answer_ids_to_remove)
    questionnaire_store_updater.save()

    list_collector_url = url_for('questionnaire.get_block', block_id=parent_block['id'])

    return list_collector_url


@questionnaire_blueprint.route('<block_id>/', methods=['POST'])
@questionnaire_blueprint.route('<list_name>/<block_id>/', methods=['POST'])
@questionnaire_blueprint.route(
    '<list_name>/<list_item_id>/<block_id>/', methods=['POST']
)
@login_required
@with_questionnaire_store
@with_schema
@section_routing_path_required
# pylint: disable=too-many-locals, too-many-return-statements, bad-continuation
def post_block(
    routing_path,
    schema,
    questionnaire_store,
    block_id,
    list_name=None,
    list_item_id=None,
):
    return post_block_handler(
        routing_path, schema, questionnaire_store, block_id, list_name, list_item_id
    )


@post_submission_blueprint.route('thank-you/', methods=['GET'])
@login_required
@with_schema
def get_thank_you(schema):
    session_data = get_session_store().session_data

    if not session_data.submitted_time:
        return redirect(url_for('questionnaire.get_questionnaire'))

    metadata_context = build_metadata_context_for_survey_completed(session_data)

    view_submission_url = None
    view_submission_duration = 0
    if _is_submission_viewable(schema.json, session_data.submitted_time):
        view_submission_url = url_for('.get_view_submission')
        view_submission_duration = humanize.naturaldelta(
            timedelta(seconds=schema.json['view_submitted_response']['duration'])
        )

    return flask_render_template(
        'thank-you.html',
        metadata=metadata_context,
        analytics_ua_id=current_app.config['EQ_UA_ID'],
        survey_id=schema.json['survey_id'],
        survey_title=safe_content(schema.json['title']),
        is_view_submitted_response_enabled=is_view_submitted_response_enabled(
            schema.json
        ),
        view_submission_url=view_submission_url,
        account_service_url=cookie_session.get('account_service_url'),
        account_service_log_out_url=cookie_session.get('account_service_log_out_url'),
        view_submission_duration=view_submission_duration,
    )


@post_submission_blueprint.route('thank-you/', methods=['POST'])
@login_required
def post_thank_you():
    if 'action[sign_out]' in request.form:
        return redirect(url_for('session.get_sign_out'))

    return redirect(url_for('post_submission.get_thank_you'))


@post_submission_blueprint.route('view-submission/', methods=['GET'])
@login_required
@with_schema
def get_view_submission(schema):  # pylint: too-many-locals

    session_data = get_session_store().session_data

    if _is_submission_viewable(schema.json, session_data.submitted_time):
        submitted_data = current_app.eq['storage'].get_by_key(
            SubmittedResponse, session_data.tx_id
        )

        if submitted_data:

            metadata_context = build_metadata_context_for_survey_completed(session_data)

            pepper = current_app.eq['secret_store'].get_secret_by_name(
                'EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER'
            )

            encrypter = StorageEncryption(
                current_user.user_id, current_user.user_ik, pepper
            )
            submitted_data = encrypter.decrypt_data(submitted_data.data)

            # for backwards compatibility
            # submitted data used to be base64 encoded before encryption
            try:
                submitted_data = base64url_decode(submitted_data.decode()).decode()
            except ValueError:
                pass

            submitted_data = json.loads(submitted_data)
            answer_store = AnswerStore(submitted_data.get('answers'))

            metadata = submitted_data.get('metadata')

            summary_rendered_context = build_summary_rendering_context(
                schema, answer_store, metadata
            )

            context = {
                'summary': {
                    'groups': summary_rendered_context,
                    'answers_are_editable': False,
                    'is_view_submission_response_enabled': is_view_submitted_response_enabled(
                        schema.json
                    ),
                }
            }

            return flask_render_template(
                'view-submission.html',
                metadata=metadata_context,
                analytics_ua_id=current_app.config['EQ_UA_ID'],
                survey_id=schema.json['survey_id'],
                survey_title=safe_content(schema.json['title']),
                account_service_url=cookie_session.get('account_service_url'),
                account_service_log_out_url=cookie_session.get(
                    'account_service_log_out_url'
                ),
                content=context,
            )

    return redirect(url_for('post_submission.get_thank_you'))


@post_submission_blueprint.route('view-submission/', methods=['POST'])
@login_required
def post_view_submission():
    if 'action[sign_out]' in request.form:
        return redirect(url_for('session.get_sign_out'))

    return redirect(url_for('post_submission.get_view_submission'))


def _set_started_at_metadata_if_required(form, collection_metadata):
    if not collection_metadata.get('started_at') and form.data:
        started_at = datetime.utcnow().isoformat()

        logger.info(
            'Survey started. Writing started_at time to collection metadata',
            started_at=started_at,
        )

        collection_metadata['started_at'] = started_at


def _render_page(block_type, context, current_location, previous_location, schema):
    if request_wants_json():
        return jsonify(context)

    return _render_template(
        context, current_location, previous_location, block_type, schema
    )


def _generate_wtf_form(form, block, schema):
    disable_mandatory = 'action[save_sign_out]' in form

    wtf_form = post_form_for_block(
        schema,
        block,
        get_answer_store(current_user),
        get_metadata(current_user),
        request.form,
        disable_mandatory,
    )

    return wtf_form


def _is_end_of_questionnaire(block):
    return block['type'] in END_BLOCKS


def submit_answers(schema):
    questionnaire_store = get_questionnaire_store(
        current_user.user_id, current_user.user_ik
    )
    answer_store = questionnaire_store.answer_store
    metadata = questionnaire_store.metadata
    full_routing_path = path_finder.full_routing_path()

    message = json.dumps(
        convert_answers(schema, questionnaire_store, full_routing_path), for_json=True
    )

    encrypted_message = encrypt(
        message, current_app.eq['key_store'], KEY_PURPOSE_SUBMISSION
    )
    sent = current_app.eq['submitter'].send_message(
        encrypted_message,
        questionnaire_id=metadata.get('questionnaire_id'),
        case_id=metadata.get('case_id'),
        tx_id=metadata.get('tx_id'),
    )

    if not sent:
        raise SubmissionFailedException()

    submitted_time = datetime.utcnow()

    _store_submitted_time_in_session(submitted_time)

    if is_view_submitted_response_enabled(schema.json):
        _store_viewable_submission(answer_store.serialise(), metadata, submitted_time)

    get_questionnaire_store(current_user.user_id, current_user.user_ik).delete()

    return redirect(url_for('post_submission.get_thank_you'))


def _store_submitted_time_in_session(submitted_time):
    session_store = get_session_store()
    session_data = session_store.session_data
    session_data.submitted_time = submitted_time.isoformat()
    session_store.save()


def _store_viewable_submission(answers, metadata, submitted_time):
    pepper = current_app.eq['secret_store'].get_secret_by_name(
        'EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER'
    )
    encrypter = StorageEncryption(current_user.user_id, current_user.user_ik, pepper)
    encrypted_data = encrypter.encrypt_data(
        {'answers': answers, 'metadata': metadata.copy()}
    )

    valid_until = submitted_time + timedelta(
        seconds=g.schema.json['view_submitted_response']['duration']
    )

    item = SubmittedResponse(
        tx_id=metadata['tx_id'],
        data=encrypted_data,
        valid_until=valid_until.replace(tzinfo=tzutc()),
    )

    current_app.eq['storage'].put(item)


def is_view_submitted_response_enabled(schema):
    view_submitted_response = schema.get('view_submitted_response')
    if view_submitted_response:
        return view_submitted_response['enabled']

    return False


def _is_submission_viewable(schema, submitted_time):
    if is_view_submitted_response_enabled(schema) and submitted_time:
        submitted_time = datetime.strptime(submitted_time, '%Y-%m-%dT%H:%M:%S.%f')
        submission_valid_until = submitted_time + timedelta(
            seconds=schema['view_submitted_response']['duration']
        )
        return submission_valid_until > datetime.utcnow()

    return False


def _save_sign_out(current_location, previous_location, block, form, schema):
    questionnaire_store = get_questionnaire_store(
        current_user.user_id, current_user.user_ik
    )

    if form.validate():
        questionnaire_store_updater = QuestionnaireStoreUpdater(
            current_location, schema, questionnaire_store, block.get('question')
        )
        questionnaire_store_updater.update_answers(form)
        # The location needs to be removed as we may have previously completed this location
        questionnaire_store_updater.remove_completed_location()
        questionnaire_store_updater.save()

        logout_user()

        return redirect(url_for('session.get_sign_out'))

    context = _get_context(block, current_location, schema, form)
    return _render_page(
        block['type'], context, current_location, previous_location, schema
    )


def _redirect_to_location(location):
    return redirect(url_for('questionnaire.get_block', block_id=location.block_id))


def _get_context(block, current_location, schema, form=None):
    questionnaire_store = get_questionnaire_store(
        current_user.user_id, current_user.user_ik
    )

    list_store = questionnaire_store.list_store
    metadata = questionnaire_store.metadata
    answer_store = questionnaire_store.answer_store

    return build_view_context(
        block['type'],
        metadata,
        schema,
        list_store,
        answer_store,
        block,
        current_location,
        form=form,
    )


def get_page_title_for_location(schema, current_location, context):
    block = schema.get_block(current_location.block_id)
    if block['type'] == 'Interstitial':
        group = schema.get_group_for_block_id(block['id'])
        page_title = '{group_title} - {survey_title}'.format(
            group_title=group['title'], survey_title=schema.json['title']
        )
    elif block['type'] == 'Question':
        question_title = context['block']['question'].get('title')

        page_title = '{question_title} - {survey_title}'.format(
            question_title=question_title, survey_title=schema.json['title']
        )
    else:
        page_title = schema.json['title']

    return safe_content(page_title)


@with_session_timeout
@with_analytics
@with_legal_basis
def _render_template(
    context, current_location, previous_location, template, schema, **kwargs
):
    page_title = get_page_title_for_location(schema, current_location, context)

    session_store = get_session_store()
    session_data = session_store.session_data

    previous_location_url = None
    if previous_location:
        previous_location_url = previous_location.url()

    return render_template(
        template,
        content=context,
        current_location=current_location,
        previous_location=previous_location_url,
        page_title=page_title,
        language_code=session_data.language_code,
        **kwargs,
    )


def request_wants_json():
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return (
        best == 'application/json'
        and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']
    )


def _render_block(
    schema, metadata, answer_store, block_id, current_location, previous_location
):
    block = schema.get_block(block_id)
    transformed_block = transform_variants(block, schema, metadata, answer_store)

    placeholder_renderer = PlaceholderRenderer(
        language=flask_babel.get_locale().language,
        answer_store=answer_store,
        metadata=metadata,
    )
    rendered_block = placeholder_renderer.render(transformed_block)

    context = _get_context(rendered_block, current_location, schema)

    return _render_page(
        rendered_block['type'], context, current_location, previous_location, schema
    )

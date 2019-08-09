from datetime import datetime, timedelta

import flask_babel
import humanize
import simplejson as json
from dateutil.tz import tzutc
from flask import Blueprint, g, redirect, request, url_for, current_app, jsonify
from flask_login import current_user, login_required
from jwcrypto.common import base64url_decode
from sdc.crypto.encrypter import encrypt
from structlog import get_logger

from app.authentication.no_token_exception import NoTokenException
from app.views.handlers.block_factory import get_block_handler
from app.data_model.answer_store import AnswerStore
from app.data_model.app_models import SubmittedResponse
from app.data_model.list_store import ListStore
from app.data_model.progress_store import CompletionStatus
from app.globals import (
    get_answer_store,
    get_metadata,
    get_questionnaire_store,
    get_session_store,
    get_session_timeout_in_seconds,
)
from app.helpers.form_helper import get_form_for_location, post_form_for_block
from app.helpers.path_finder_helper import path_finder
from app.helpers.schema_helpers import with_schema
from app.helpers.session_helpers import with_questionnaire_store
from app.helpers.template_helper import render_template, safe_content
from app.keys import KEY_PURPOSE_SUBMISSION
from app.questionnaire.location import InvalidLocationException, Location
from app.questionnaire.router import Router
from app.questionnaire.relationship_location import RelationshipLocation
from app.storage.storage_encryption import StorageEncryption
from app.submitter.converter import convert_answers
from app.submitter.submission_failed import SubmissionFailedException
from app.views.contexts.metadata_context import (
    build_metadata_context_for_survey_completed,
)
from app.views.contexts.summary_context import build_summary_rendering_context
from app.views.contexts.hub_context import HubContext
from app.utilities.schema import load_schema_from_session_data

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
    router = Router(
        schema,
        progress_store=questionnaire_store.progress_store,
        list_store=questionnaire_store.list_store,
    )
    completed_section_ids = questionnaire_store.progress_store.completed_section_ids
    hub_required_sections_complete = all(
        section_id in completed_section_ids
        for section_id in schema.get_hub_required_section_ids()
    )

    if not schema.is_hub_enabled() or not hub_required_sections_complete:
        redirect_location = router.get_first_incomplete_location_in_survey()
        return redirect(redirect_location.url())

    language_code = get_session_store().session_data.language_code
    hub = HubContext(
        questionnaire_store.progress_store,
        schema.get_sections(),
        router.is_survey_complete(),
    )

    return render_template(
        'hub', content=hub.get_context(), language_code=language_code
    )


@questionnaire_blueprint.route('/', methods=['POST'])
@login_required
@with_questionnaire_store
@with_schema
def post_questionnaire(schema, questionnaire_store):
    if any(
        action in request.form
        for action in ('action[save_sign_out]', 'action[sign_out]')
    ):
        return redirect(url_for('session.get_sign_out'))

    router = Router(
        schema,
        progress_store=questionnaire_store.progress_store,
        list_store=questionnaire_store.list_store,
    )

    if schema.is_hub_enabled() and router.is_survey_complete():
        return submit_answers(schema)

    return redirect(router.get_first_incomplete_location_in_survey().url())


@questionnaire_blueprint.route('sections/<section_id>/', methods=['GET'])
@login_required
@with_questionnaire_store
@with_schema
def get_section(schema, questionnaire_store, section_id):

    progress_store = questionnaire_store.progress_store
    router = Router(
        schema, progress_store=progress_store, list_store=questionnaire_store.list_store
    )

    if not schema.is_hub_enabled():
        redirect_location = router.get_first_incomplete_location_in_survey()
        return redirect(redirect_location.url())

    section = schema.get_section(section_id)
    if not section:
        return redirect(url_for('.get_questionnaire'))

    section_status = progress_store.get_section_status(section_id)
    routing_path = path_finder.routing_path(section)

    if section_status == CompletionStatus.COMPLETED:
        return redirect(routing_path[-1].url())

    if section_status == CompletionStatus.NOT_STARTED:
        return redirect(
            router.get_first_incomplete_location_for_section(
                section_id, routing_path
            ).url()
        )

    return redirect(
        router.get_last_complete_location_for_section(section_id, routing_path).url()
    )


# pylint: disable=too-many-return-statements
@questionnaire_blueprint.route('<block_id>/', methods=['GET', 'POST'])
@questionnaire_blueprint.route('<list_name>/<block_id>/', methods=['GET', 'POST'])
@questionnaire_blueprint.route(
    '<list_name>/<list_item_id>/<block_id>/', methods=['GET', 'POST']
)
@login_required
@with_questionnaire_store
@with_schema
def block(schema, questionnaire_store, block_id, list_name=None, list_item_id=None):
    current_location = Location(
        block_id=block_id, list_name=list_name, list_item_id=list_item_id
    )

    try:
        block_handler = get_block_handler(
            schema=schema,
            location=current_location,
            questionnaire_store=questionnaire_store,
            language=flask_babel.get_locale().language,
        )
    except InvalidLocationException:
        return redirect(url_for('.get_questionnaire'))

    if block_handler.rendered_block['type'] == 'RelationshipCollector':
        return redirect(block_handler.get_first_location_url())

    if 'action[sign_out]' in request.form:
        return redirect(url_for('session.get_sign_out'))

    form = _generate_wtf_form(block_handler.rendered_block, schema, current_location)
    if request.method == 'GET' or not form.validate():
        return _render_page(
            block_type=block_handler.rendered_block['type'],
            context=block_handler.get_context(form),
            current_location=current_location,
            previous_location_url=block_handler.get_previous_location_url(),
            schema=schema,
        )

    if 'action[save_sign_out]' in request.form:
        block_handler.save_on_signout(form)
        return redirect(url_for('session.get_sign_out'))

    if block_handler.rendered_block['type'] in END_BLOCKS:
        return submit_answers(schema)

    if form.data:
        block_handler.set_started_at_metadata()

    block_handler.handle_post(form)
    next_location_url = block_handler.get_next_location_url()

    return redirect(next_location_url)


@questionnaire_blueprint.route(
    '<block_id>/<from_list_item_id>/to/<to_list_item_id>/', methods=['GET', 'POST']
)
@login_required
@with_questionnaire_store
@with_schema
def relationship(
    schema, questionnaire_store, block_id, from_list_item_id, to_list_item_id
):
    current_location = RelationshipLocation(
        block_id, from_list_item_id, to_list_item_id
    )

    try:
        block_handler = get_block_handler(
            schema=schema,
            location=current_location,
            questionnaire_store=questionnaire_store,
            language=flask_babel.get_locale().language,
        )
    except InvalidLocationException:
        return redirect(url_for('.get_questionnaire'))

    form = _generate_wtf_form(block_handler.rendered_block, schema, current_location)
    if request.method == 'GET' or not form.validate():
        return _render_page(
            block_type=block_handler.rendered_block['type'],
            context=block_handler.get_context(form),
            current_location=current_location,
            previous_location_url=block_handler.get_previous_location_url(),
            schema=schema,
        )

    if 'action[save_sign_out]' in request.form:
        block_handler.save_on_signout(form)
        return redirect(url_for('session.get_sign_out'))

    block_handler.handle_post(form)
    next_location_url = block_handler.get_next_location_url()
    return redirect(next_location_url)


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

    return render_template(
        template='thank-you',
        metadata=metadata_context,
        survey_id=schema.json['survey_id'],
        survey_title=safe_content(schema.json['title']),
        is_view_submitted_response_enabled=is_view_submitted_response_enabled(
            schema.json
        ),
        view_submission_url=view_submission_url,
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
            list_store = ListStore(submitted_data.get('lists'))

            metadata = submitted_data.get('metadata')

            summary_rendered_context = build_summary_rendering_context(
                schema, answer_store, list_store, metadata
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

            return render_template(
                template='view-submission',
                metadata=metadata_context,
                content=context,
                survey_id=schema.json['survey_id'],
                survey_title=safe_content(schema.json['title']),
            )

    return redirect(url_for('post_submission.get_thank_you'))


@post_submission_blueprint.route('view-submission/', methods=['POST'])
@login_required
def post_view_submission():
    if 'action[sign_out]' in request.form:
        return redirect(url_for('session.get_sign_out'))

    return redirect(url_for('post_submission.get_view_submission'))


def _generate_wtf_form(block_schema, schema, current_location):
    answer_store = get_answer_store(current_user)
    metadata = get_metadata(current_user)

    if request.method == 'POST':
        disable_mandatory = 'action[save_sign_out]' in request.form
        return post_form_for_block(
            schema,
            block_schema,
            answer_store,
            metadata,
            request.form,
            disable_mandatory,
        )
    return get_form_for_location(
        schema, block_schema, current_location, answer_store, metadata
    )


def submit_answers(schema):
    questionnaire_store = get_questionnaire_store(
        current_user.user_id, current_user.user_ik
    )
    answer_store = questionnaire_store.answer_store
    list_store = questionnaire_store.list_store
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
        _store_viewable_submission(
            answer_store.serialise(), list_store.serialise(), metadata, submitted_time
        )

    get_questionnaire_store(current_user.user_id, current_user.user_ik).delete()

    return redirect(url_for('post_submission.get_thank_you'))


def _store_submitted_time_in_session(submitted_time):
    session_store = get_session_store()
    session_data = session_store.session_data
    session_data.submitted_time = submitted_time.isoformat()
    session_store.save()


def _store_viewable_submission(answers, lists, metadata, submitted_time):
    pepper = current_app.eq['secret_store'].get_secret_by_name(
        'EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER'
    )
    encrypter = StorageEncryption(current_user.user_id, current_user.user_ik, pepper)
    encrypted_data = encrypter.encrypt_data(
        {'answers': answers, 'lists': lists, 'metadata': metadata.copy()}
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


def get_page_title_for_location(schema, current_location, context):
    block_schema = schema.get_block(current_location.block_id)
    if block_schema['type'] == 'Interstitial':
        group = schema.get_group_for_block_id(block_schema['id'])
        page_title = '{group_title} - {survey_title}'.format(
            group_title=group['title'], survey_title=schema.json['title']
        )
    elif block_schema['type'] == 'Question':
        question_title = context['block']['question'].get('title')

        page_title = '{question_title} - {survey_title}'.format(
            question_title=question_title, survey_title=schema.json['title']
        )
    else:
        page_title = schema.json['title']

    return safe_content(page_title)


def _render_page(block_type, context, current_location, previous_location_url, schema):
    if request_wants_json():
        return jsonify(context)

    page_title = get_page_title_for_location(schema, current_location, context)
    session_data = get_session_store().session_data
    session_timeout = get_session_timeout_in_seconds(schema)

    return render_template(
        template=block_type,
        content=context,
        current_location=current_location,
        previous_location_url=previous_location_url,
        page_title=page_title,
        language_code=session_data.language_code,
        session_timeout=session_timeout,
        survey_title=schema.json.get('title'),
        legal_basis=schema.json.get('legal_basis'),
    )


def request_wants_json():
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return (
        best == 'application/json'
        and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']
    )

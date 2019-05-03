from datetime import datetime, timedelta

from dateutil.tz import tzutc
from quart import g, current_app, session as cookie_session
from structlog import get_logger

from app.data_model.questionnaire_store import QuestionnaireStore
from app.settings import EQ_SESSION_ID, USER_IK

logger = get_logger()


def get_questionnaire_store(user_id, user_ik):
    from app.storage.encrypted_questionnaire_storage import EncryptedQuestionnaireStorage

    # Sets up a single QuestionnaireStore instance per request.
    store = g.get('_questionnaire_store')
    if store is None:
        pepper = current_app.eq['secret_store'].get_secret_by_name('EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER')
        storage = EncryptedQuestionnaireStorage(user_id, user_ik, pepper)
        store = g._questionnaire_store = QuestionnaireStore(storage)
        store.load_user_data()

    return store


async def get_questionnaire_store_async(user_id, user_ik):
    from app.storage.encrypted_questionnaire_storage import EncryptedQuestionnaireStorage

    # Sets up a single QuestionnaireStore instance per request.
    store = g.get('_questionnaire_store')
    if store is None:
        pepper = current_app.eq['secret_store'].get_secret_by_name('EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER')
        storage = EncryptedQuestionnaireStorage(user_id, user_ik, pepper)
        store = g._questionnaire_store = QuestionnaireStore(storage)
        await store.load_user_data_async()

    return store


def get_session_store():
    from app.data_model.session_store import SessionStore

    if USER_IK not in cookie_session or EQ_SESSION_ID not in cookie_session:
        return None

    # Sets up a single SessionStore instance per request.
    store = g.get('_session_store')

    if store is None:
        pepper = current_app.eq['secret_store'].get_secret_by_name('EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER')
        store = g._session_store = SessionStore(cookie_session[USER_IK], pepper, cookie_session[EQ_SESSION_ID])
        store.load()

    return store


async def get_session_store_async():
    from app.data_model.session_store import SessionStore

    if USER_IK not in cookie_session or EQ_SESSION_ID not in cookie_session:
        return None

    # Sets up a single SessionStore instance per request.
    store = g.get('_session_store')

    if store is None:
        pepper = current_app.eq['secret_store'].get_secret_by_name('EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER')
        store = g._session_store = SessionStore(cookie_session[USER_IK], pepper, cookie_session[EQ_SESSION_ID])
        await store.load_async()

    return store


def get_session_timeout_in_seconds(schema):
    """
    Gets the session timeout in seconds from the schema/env variable.
    :return: Timeout in seconds
    """
    default_session_timeout = current_app.config['EQ_SESSION_TIMEOUT_SECONDS']
    schema_session_timeout = schema.json.get('session_timeout_in_seconds')
    timeout = schema_session_timeout if schema_session_timeout and \
        schema_session_timeout < default_session_timeout else \
        default_session_timeout

    return timeout


def create_session_store(eq_session_id, user_id, user_ik, session_data):
    from app.data_model.session_store import SessionStore

    pepper = current_app.eq['secret_store'].get_secret_by_name('EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER')
    session_timeout_in_seconds = get_session_timeout_in_seconds(g.schema)
    expires_at = datetime.now(tz=tzutc()) + timedelta(seconds=session_timeout_in_seconds)

    # pylint: disable=W0212
    g._session_store = SessionStore(user_ik, pepper).create(eq_session_id, user_id, session_data, expires_at).save()


async def create_session_store_async(eq_session_id, user_id, user_ik, session_data):
    from app.data_model.session_store import SessionStore

    pepper = current_app.eq['secret_store'].get_secret_by_name('EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER')
    session_timeout_in_seconds = get_session_timeout_in_seconds(g.schema)
    expires_at = datetime.now(tz=tzutc()) + timedelta(seconds=session_timeout_in_seconds)

    # pylint: disable=W0212
    g._session_store = SessionStore(user_ik, pepper).create(eq_session_id, user_id, session_data, expires_at)
    await g._session_store.save_async()


def get_metadata(user):
    if user.is_anonymous:
        logger.debug('anonymous user requesting metadata get instance')
        return None

    questionnaire_store = get_questionnaire_store(user.user_id, user.user_ik)
    return questionnaire_store.metadata


async def get_metadata_async(user):
    if user.is_anonymous:
        logger.debug('anonymous user requesting metadata get instance')
        return None

    questionnaire_store = await get_questionnaire_store_async(user.user_id, user.user_ik)
    return questionnaire_store.metadata


def get_collection_metadata(user):
    questionnaire_store = get_questionnaire_store(user.user_id, user.user_ik)
    return questionnaire_store.collection_metadata


async def get_collection_metadata_async(user):
    questionnaire_store = await get_questionnaire_store_async(user.user_id, user.user_ik)
    return questionnaire_store.collection_metadata


async def get_answer_store_async(user):
    questionnaire_store = await get_questionnaire_store_async(user.user_id, user.user_ik)
    return questionnaire_store.answer_store


async def get_completed_blocks_async(user):
    questionnaire_store = await get_questionnaire_store_async(user.user_id, user.user_ik)
    return questionnaire_store.completed_blocks

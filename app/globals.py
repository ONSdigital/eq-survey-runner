from flask import g, current_app, session as cookie_session
from structlog import get_logger
from app.settings import EQ_SESSION_ID

from app.data_model.questionnaire_store import QuestionnaireStore
from app.data_model.session_store import SessionStore
from app.storage.encrypted_questionnaire_storage import EncryptedQuestionnaireStorage

logger = get_logger()


def get_questionnaire_store(user_id, user_ik):
    # Sets up a single QuestionnaireStore instance per request.
    store = g.get('_questionnaire_store')
    if store is None:
        pepper = current_app.eq['secret_store'].get_secret_by_name('EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER')
        storage = EncryptedQuestionnaireStorage(user_id, user_ik, pepper)
        store = g._questionnaire_store = QuestionnaireStore(storage)

    return store


def get_session_store():
    if EQ_SESSION_ID not in cookie_session:
        return None

    # Sets up a single SessionStore instance per request.
    store = g.get('_session_store')

    if store is None:
        store = g._session_store = SessionStore(cookie_session[EQ_SESSION_ID])

    return store


def create_session_store(eq_session_id, user_id, session_data):
    # pylint: disable=W0212
    g._session_store = SessionStore().create(eq_session_id, user_id, session_data).save()


def get_metadata(user):
    if user.is_anonymous:
        logger.debug('anonymous user requesting metadata get instance')
        return None

    questionnaire_store = get_questionnaire_store(user.user_id, user.user_ik)
    return questionnaire_store.metadata


def get_answer_store(user):
    questionnaire_store = get_questionnaire_store(user.user_id, user.user_ik)

    if questionnaire_store.version < questionnaire_store.LATEST_VERSION:
        questionnaire_store.answer_store.upgrade(questionnaire_store.version, g.schema_json)
        questionnaire_store.version = questionnaire_store.LATEST_VERSION

    return questionnaire_store.answer_store


def get_completed_blocks(user):
    questionnaire_store = get_questionnaire_store(user.user_id, user.user_ik)
    return questionnaire_store.completed_blocks

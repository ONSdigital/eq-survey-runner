from flask import g, current_app, session as cookie_session
from structlog import get_logger
from app.settings import EQ_SESSION_ID, USER_IK

from app.data_model.questionnaire_store import QuestionnaireStore
from app.questionnaire.completeness import Completeness

logger = get_logger()


def get_questionnaire_store(user_id, user_ik):
    from app.storage.encrypted_questionnaire_storage import EncryptedQuestionnaireStorage

    # Sets up a single QuestionnaireStore instance per request.
    store = g.get('_questionnaire_store')
    if store is None:
        pepper = current_app.eq['secret_store'].get_secret_by_name('EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER')
        storage = EncryptedQuestionnaireStorage(user_id, user_ik, pepper)
        store = g._questionnaire_store = QuestionnaireStore(storage)

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

    return store


def create_session_store(eq_session_id, user_id, user_ik, session_data):
    from app.data_model.session_store import SessionStore

    # pylint: disable=W0212
    pepper = current_app.eq['secret_store'].get_secret_by_name('EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER')
    g._session_store = SessionStore(user_ik, pepper).create(eq_session_id, user_id, session_data).save()  # pylint: disable=assignment-from-no-return


def get_metadata(user):
    if user.is_anonymous:
        logger.debug('anonymous user requesting metadata get instance')
        return None

    questionnaire_store = get_questionnaire_store(user.user_id, user.user_ik)
    return questionnaire_store.metadata


def get_answer_store(user):
    questionnaire_store = get_questionnaire_store(user.user_id, user.user_ik)

    if questionnaire_store.version < questionnaire_store.get_latest_version_number():
        questionnaire_store.answer_store.upgrade(questionnaire_store.version, g.schema)
        questionnaire_store.version = questionnaire_store.get_latest_version_number()

    return questionnaire_store.answer_store


def get_completed_blocks(user):
    questionnaire_store = get_questionnaire_store(user.user_id, user.user_ik)
    return questionnaire_store.completed_blocks


def get_completeness(user):
    from app.helpers.path_finder_helper import path_finder

    completeness_object = g.get('_completeness')

    if completeness_object is None:
        metadata = get_metadata(user)
        answer_store = get_answer_store(user)
        completed_blocks = get_completed_blocks(user)
        routing_path = path_finder.get_full_routing_path()

        completeness_object = g._completeness = Completeness(
            g.schema, answer_store, completed_blocks, routing_path, metadata)

    return completeness_object

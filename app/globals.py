from flask import g, current_app
from structlog import get_logger

from app.data_model.questionnaire_store import QuestionnaireStore
from app.storage.encrypted_questionnaire_storage import EncryptedQuestionnaireStorage

logger = get_logger()


def get_questionnaire_store(user_id, user_ik):
    # Sets up a single QuestionnaireStore instance throughout app.
    store = g.get('_questionnaire_store')
    if store is None:
        pepper = current_app.config['EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER']
        storage = EncryptedQuestionnaireStorage(current_app.eq['database'], user_id, user_ik, pepper)
        store = g._questionnaire_store = QuestionnaireStore(storage)

    return store


def get_metadata(user):
    if user.is_anonymous:
        logger.debug("anonymous user requesting metadata get instance")
        return None

    questionnaire_store = get_questionnaire_store(user.user_id, user.user_ik)
    return questionnaire_store.metadata


def get_answer_store(user):
    questionnaire_store = get_questionnaire_store(user.user_id, user.user_ik)

    return questionnaire_store.answer_store


def get_completed_blocks(user):
    questionnaire_store = get_questionnaire_store(user.user_id, user.user_ik)
    return questionnaire_store.completed_blocks

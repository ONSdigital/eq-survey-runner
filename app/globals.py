import logging

from app.data_model.questionnaire_store import QuestionnaireStore

from flask import g

logger = logging.getLogger(__name__)


def get_questionnaire_store(user_id, user_ik):
    # Sets up a single QuestionnaireStore instance throughout app.
    store = g.get('_questionnaire_store')
    if store is None:
        try:
            store = g._questionnaire_store = QuestionnaireStore(user_id, user_ik)
        except ValueError as e:
            logger.error("questionnaire_store failed to init", exception=repr(e))

    return store


def get_metadata(user):
    if user.is_anonymous:
        logger.debug("Anonymous user requesting metadata get instance")
        return None

    questionnaire_store = get_questionnaire_store(user.user_id, user.user_ik)
    return questionnaire_store.metadata


def get_answer_store(user):
    questionnaire_store = get_questionnaire_store(user.user_id, user.user_ik)

    return questionnaire_store.answer_store


def get_answers(user):
    return get_answer_store(user).map()


def get_completed_blocks(user):
    questionnaire_store = get_questionnaire_store(user.user_id, user.user_ik)
    return questionnaire_store.completed_blocks

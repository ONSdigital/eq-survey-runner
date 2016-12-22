import logging

from app import settings
from app.storage.encrypted_questionnaire_storage import EncryptedQuestionnaireStorage
from app.storage.questionnaire_storage import QuestionnaireStorage

logger = logging.getLogger(__name__)


def get_storage(user_id, user_ik):
    if settings.EQ_SERVER_SIDE_STORAGE_ENCRYPTION:
        return EncryptedQuestionnaireStorage(user_id, user_ik)
    else:
        return QuestionnaireStorage(user_id)

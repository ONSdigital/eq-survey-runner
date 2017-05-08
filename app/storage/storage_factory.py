from app.storage.encrypted_questionnaire_storage import EncryptedQuestionnaireStorage
from app.storage.questionnaire_storage import QuestionnaireStorage


def get_storage(user_id, user_ik, use_encrypted_storage=False, pepper=''):
    if use_encrypted_storage:
        return EncryptedQuestionnaireStorage(user_id, user_ik, pepper)
    else:
        return QuestionnaireStorage(user_id)

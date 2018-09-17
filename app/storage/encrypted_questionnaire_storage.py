import snappy

from structlog import get_logger

from app.data_model.app_models import QuestionnaireState
from app.storage import data_access
from app.storage.storage_encryption import StorageEncryption
logger = get_logger()


class EncryptedQuestionnaireStorage:

    def __init__(self, user_id, user_ik, pepper):
        if user_id is None:
            raise ValueError('User id must be set')

        self._user_id = user_id
        self.encrypter = StorageEncryption(user_id, user_ik, pepper)

    def add_or_update(self, data, version):
        encrypted_data = self.encrypter.encrypt_data(snappy.compress(data))
        questionnaire_state = QuestionnaireState(self._user_id, encrypted_data, version)

        data_access.put(questionnaire_state)

    def get_user_data(self):
        questionnaire_state = self._find_questionnaire_state()
        if questionnaire_state:
            version = questionnaire_state.version or 0

            decrypted_data = snappy.uncompress(self.encrypter.decrypt_data(questionnaire_state.state_data))
            return decrypted_data, version

        return None, None

    def delete(self):
        logger.debug('deleting users data', user_id=self._user_id)
        questionnaire_state = self._find_questionnaire_state()
        if questionnaire_state:
            data_access.delete(questionnaire_state)

    def _find_questionnaire_state(self):
        logger.debug('getting questionnaire data', user_id=self._user_id)
        return data_access.get_by_key(QuestionnaireState, self._user_id)

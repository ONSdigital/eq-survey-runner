import json
import snappy

from structlog import get_logger
from jwcrypto.common import base64url_decode

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
        json_data = json.loads(data)
        json_metadata = json_data['METADATA']

        collection_exercise_id = json_metadata['collection_exercise_sid']
        form_type = json_metadata['form_type']
        eq_id = json_metadata['eq_id']
        ru_ref = json_metadata['ru_ref']

        compressed_data = snappy.compress(data)
        encrypted_data = self.encrypter.encrypt_data(compressed_data)
        questionnaire_state = self._find_questionnaire_state()

        if questionnaire_state:
            logger.debug('updating questionnaire data', user_id=self._user_id)
            questionnaire_state.state_data = encrypted_data
            questionnaire_state.version = version
        else:
            logger.debug('creating questionnaire data', user_id=self._user_id)
            questionnaire_state = QuestionnaireState(self._user_id, encrypted_data, version, collection_exercise_id, form_type, ru_ref, eq_id)

        data_access.put(questionnaire_state)

    def get_user_data(self):
        questionnaire_state = self._find_questionnaire_state()
        if questionnaire_state and questionnaire_state.state_data:
            version = questionnaire_state.version or 0

            if version < 3:
                decrypted_data = self._get_base64_encoded_data(questionnaire_state.state_data)
            else:
                decrypted_data = self._get_snappy_compressed_data(questionnaire_state.state_data)

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

    def _get_base64_encoded_data(self, data):
        """
        Legacy data was stored in a dict, base64-encoded, and not compressed:
        { 'data': '<base 64 encoded and encrypted data' }
        """
        data = json.loads(data).get('data')
        decrypted_data = self.encrypter.decrypt_data(data)
        return base64url_decode(decrypted_data.decode()).decode()

    def _get_snappy_compressed_data(self, data):
        decrypted_data = self.encrypter.decrypt_data(data)
        return snappy.uncompress(decrypted_data).decode()

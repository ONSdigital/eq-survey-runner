import snappy
import os
from quart import current_app

from structlog import get_logger
from gcloud.aio import datastore as async_datastore

from app.data_model.app_models import QuestionnaireState
from app.data_model.questionnaire_store import QuestionnaireStore
from app.storage.storage_encryption import StorageEncryption
from app.storage.async_datastore import AsyncDatastoreStorage
logger = get_logger()


class EncryptedQuestionnaireStorage:

    def __init__(self, user_id, user_ik, pepper):
        if user_id is None:
            raise ValueError('User id must be set')

        self._user_id = user_id
        self.encrypter = StorageEncryption(user_id, user_ik, pepper)

    def add_or_update(self, data):
        compressed_data = snappy.compress(data)
        encrypted_data = self.encrypter.encrypt_data(compressed_data)
        questionnaire_state = self._find_questionnaire_state()
        if questionnaire_state:
            logger.debug('updating questionnaire data', user_id=self._user_id)
            questionnaire_state.state_data = encrypted_data
        else:
            logger.debug('creating questionnaire data', user_id=self._user_id)
            questionnaire_state = QuestionnaireState(self._user_id, encrypted_data, QuestionnaireStore.LATEST_VERSION)

        current_app.eq['storage'].put(questionnaire_state)

    async def add_or_update_async(self, data):
        compressed_data = snappy.compress(data)
        encrypted_data = self.encrypter.encrypt_data(compressed_data)
        questionnaire_state = await self._find_questionnaire_state_async()
        if questionnaire_state:
            logger.debug('updating questionnaire data', user_id=self._user_id)
            questionnaire_state.state_data = encrypted_data
        else:
            logger.debug('creating questionnaire data', user_id=self._user_id)
            questionnaire_state = QuestionnaireState(self._user_id, encrypted_data, QuestionnaireStore.LATEST_VERSION)

        client = async_datastore.Datastore(os.getenv('EQ_DATASTORE_PROJECT_ID'))
        async_storage = AsyncDatastoreStorage(client)

        await async_storage.put(questionnaire_state)

    def get_user_data(self):
        questionnaire_state = self._find_questionnaire_state()
        if questionnaire_state and questionnaire_state.state_data:
            version = questionnaire_state.version
            decrypted_data = self._get_snappy_compressed_data(questionnaire_state.state_data)
            return decrypted_data, version

        return None, None

    async def get_user_data_async(self):
        questionnaire_state = await self._find_questionnaire_state_async()
        if questionnaire_state and questionnaire_state.state_data:
            version = questionnaire_state.version
            decrypted_data = self._get_snappy_compressed_data(questionnaire_state.state_data)
            return decrypted_data, version

        return None, None

    def delete(self):
        logger.debug('deleting users data', user_id=self._user_id)
        questionnaire_state = self._find_questionnaire_state()
        if questionnaire_state:
            current_app.eq['storage'].delete(questionnaire_state)

    async def delete_async(self):
        logger.debug('deleting users data', user_id=self._user_id)
        questionnaire_state = self._find_questionnaire_state_async()
        if questionnaire_state:
            client = async_datastore.Datastore(os.getenv('EQ_DATASTORE_PROJECT_ID'))
            async_storage = AsyncDatastoreStorage(client)
            await async_storage.delete(questionnaire_state)

    def _find_questionnaire_state(self):
        logger.debug('getting questionnaire data', user_id=self._user_id)
        return current_app.eq['storage'].get_by_key(QuestionnaireState, self._user_id)

    async def _find_questionnaire_state_async(self):
        logger.debug('getting questionnaire data async', user_id=self._user_id)

        client = async_datastore.Datastore(os.getenv('EQ_DATASTORE_PROJECT_ID'))
        async_storage = AsyncDatastoreStorage(client)

        return await async_storage.get_by_key(QuestionnaireState, self._user_id)

    def _get_snappy_compressed_data(self, data):
        decrypted_data = self.encrypter.decrypt_data(data)
        return snappy.uncompress(decrypted_data).decode()

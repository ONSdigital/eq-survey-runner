import logging

from app.storage.storage_factory import get_storage
from app.data_model.answer_store import AnswerStore

logger = logging.getLogger(__name__)


class QuestionnaireStore:

    def __init__(self, user_id, user_ik):

        self.metadata_store = {}
        self.answer_store = AnswerStore()
        self.completed_block_store = []

        if user_id and user_ik:
            self.user_id = user_id
            self.user_ik = user_ik
        else:
            raise ValueError("No user_id or user_ik found in session")

        self.storage = get_storage()

        if self.storage.has_data(self.user_id):
            logger.debug("User %s has previous data loading", user_id)
            data = self.storage.get(self.user_id, self.user_ik)

            if 'METADATA' in data:
                self.metadata = data['METADATA']

            if 'ANSWERS' in data:
                self.answer_store.answers = data['ANSWERS']

            if 'COMPLETED_BLOCKS' in data:
                self.completed_block_store = data['COMPLETED_BLOCKS']

    def delete(self):
        logger.debug("Deleting questionnaire data for %s", self.user_id)
        self.storage.delete(self.user_id)

    def save(self):
        data = {
            "METADATA": self.metadata,
            "ANSWERS": self.answers.answers,
            "COMPLETED_BLOCKS": self.completed_blocks
        }
        logger.debug("Saving user data %s for user id %s", data, self.user_id)
        self.storage.store(data=data, user_id=self.user_id, user_ik=self.user_ik)

    @property
    def metadata(self):
        return self.metadata_store

    @metadata.setter
    def metadata(self, metadata):
        self.metadata_store = metadata

    @property
    def answers(self):
        return self.answer_store

    @property
    def completed_blocks(self):
        return self.completed_block_store

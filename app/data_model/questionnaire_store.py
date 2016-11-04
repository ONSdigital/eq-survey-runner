import logging

from app.storage.storage_factory import get_storage

logger = logging.getLogger(__name__)


class QuestionnaireStore:

    def __init__(self, user_id, user_ik):
        self.data = {}

        if user_id and user_ik:
            self.user_id = user_id
            self.user_ik = user_ik
        else:
            raise ValueError("No user_id or user_ik found in session")

        self.storage = get_storage()

        if self.storage.has_data(self.user_id):
            logger.debug("User %s has previous data loading", user_id)
            self.data = self.storage.get(self.user_id, self.user_ik)

    def delete(self):
        logger.debug("Deleting questionnaire data for %s", self.user_id)
        self.data = {}
        self.storage.delete(self.user_id)

    def save(self):
        logger.debug("Saving user data %s for user id %s", self.data, self.user_id)
        self.storage.store(data=self.data, user_id=self.user_id, user_ik=self.user_ik)

    @property
    def metadata(self):
        if "METADATA" in self.data:
            return self.data["METADATA"]
        else:
            raise RuntimeError("No metadata for user %s", self.user_id)

    @metadata.setter
    def metadata(self, metadata):
        self.data["METADATA"] = metadata

    @property
    def answers(self):
        if "ANSWERS" not in self.data:
            self.data["ANSWERS"] = {}

        return self.data["ANSWERS"]

    @property
    def completed_blocks(self):
        if "COMPLETED_BLOCKS" not in self.data:
            self.data["COMPLETED_BLOCKS"] = []

        return self.data["COMPLETED_BLOCKS"]

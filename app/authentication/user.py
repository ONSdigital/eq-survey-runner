import logging

from app.storage.storage_factory import StorageFactory

from flask_login import UserMixin

logger = logging.getLogger(__name__)


class User(UserMixin):
    def __init__(self, user_id, user_ik):
        if user_id and user_ik:
            self.user_id = user_id
            self.user_ik = user_ik
        else:
            raise ValueError("No user_id or user_ik found in session")


class QuestionnaireData:

    def __init__(self, user_id, user_ik):
        self.data = {}

        if user_id and user_ik:
            self.user_id = user_id
            self.user_ik = user_ik
        else:
            raise ValueError("No user_id or user_ik found in session")

        self.storage = StorageFactory.get_storage_mechanism()

        if self.storage.has_data(self.user_id):
            logger.debug("User %s has previous data loading", user_id)
            self.load()
        else:
            logger.debug("User %s does not have previous data creating", user_id)
            self.save()

    def delete(self):
        logger.debug("Deleting questionnaire data for %s", self.user_id)
        self.data = {}
        self.storage.delete(self.user_id)

    def save(self):
        logger.debug("Saving user data %s for user id %s", self.data, self.user_id)
        self.storage.store(data=self.data, user_id=self.user_id, user_ik=self.user_ik)

    def load(self):
        self.data = self.storage.get(self.user_id, self.user_ik)
        logger.debug("Loaded questionnaire data %s", self.data)

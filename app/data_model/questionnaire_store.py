import logging

from app.storage.storage_factory import get_storage

from flask import g

import jsonpickle

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

    def encode_metadata(self, metadata):
        self.data["METADATA"] = jsonpickle.encode(metadata)

    def decode_metadata(self):
        if "METADATA" in self.data:
            return jsonpickle.decode(self.data["METADATA"])
        else:
            raise RuntimeError("No metadata for user %s", self.user_id)


def get_questionnaire_store(user_id, user_ik):
    # Sets up a single QuestionnaireStore instance throughout app.
    store = g.get('_questionnaire_store')
    if store is None:
        try:
            store = g._questionnaire_store = QuestionnaireStore(user_id, user_ik)
        except Exception as e:
            logger.error("questionnaire_store failed to init", exception=repr(e))

    return store


def get_metadata(user):
    try:
        questionnaire_store = get_questionnaire_store(user.user_id, user.user_ik)
        return questionnaire_store.decode_metadata()
    except AttributeError:
        logger.debug("Anonymous user requesting metadata get instance")
        # anonymous user mixin - this happens on the error pages before authentication
        return None

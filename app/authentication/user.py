from flask.ext.login import UserMixin
from app.storage.storage_factory import StorageFactory


class User(UserMixin):

    def __init__(self, user_id):
        if user_id:
            self.user_id = user_id
        else:
            raise ValueError("No user_id found in session")

        self.storage = StorageFactory.get_storage_mechanism()

        if self.storage.has_data(self.user_id):
            self.questionnaire_data = self.storage.get(self.user_id)
        else:
            self.questionnaire_data = {}
        self.save()

    def get_user_id(self):
        return self.user_id

    def get_questionnaire_data(self):
        self.questionnaire_data = self.storage.get(self.user_id)
        return self.questionnaire_data

    def delete_questionnaire_data(self):
        self.questionnaire_data = {}
        self.storage.delete(self.user_id)

    def save(self):
        self.storage.store(self.questionnaire_data, self.user_id)

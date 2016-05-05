from flask.ext.login import UserMixin
from app.storage.database_storage import DatabaseStore
from app.storage.session_storage import FlaskSessionStore
from app.storage.memory_storage import InMemoryStorage
from app import settings


class User(UserMixin):

    def __init__(self, user_id):
        if user_id:
            self.user_id = user_id
        else:
            raise ValueError("No user_id found in session")

        if settings.EQ_SERVER_SIDE_STORAGE:
            if settings.EQ_SERVER_SIDE_STORAGE_TYPE.upper() == 'DATABASE':
                self.storage = DatabaseStore()
            else:
                self.storage = InMemoryStorage()
        else:
            self.storage = FlaskSessionStore()

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

    def save(self):
        self.storage.store(self.questionnaire_data, self.user_id)

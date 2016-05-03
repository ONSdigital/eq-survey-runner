from flask.ext.login import UserMixin
from flask import session


class TemporarySessionStore(object):

    def store(self, data):
        session["questionnaire-data"] = data

    def get(self):
        return session["questionnaire-data"]

    def has_data(self):
        return "questionnaire-data" in session


class User(UserMixin):

    def __init__(self, user_id):
        if user_id:
            self.user_id = user_id
        else:
            raise ValueError("No user_id found in session")
        temp_store = TemporarySessionStore()
        if temp_store.has_data():
            self.questionnaire_data = temp_store.get()
        else:
            self.questionnaire_data = {}

    def get_user_id(self):
        return self.user_id

    def get_questionnaire_data(self):
        return self.questionnaire_data

    def save(self):
        temp_store = TemporarySessionStore()
        temp_store.store(self.questionnaire_data)

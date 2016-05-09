from flask import session
from app.storage.abstract_server_storage import AbstractServerStorage


class FlaskSessionStore(AbstractServerStorage):
    '''
    Client side storage using sessions
    '''

    def store(self, user_id, data):
        session["questionnaire-data"] = data

    def get(self, user_id):
        return session["questionnaire-data"]

    def has_data(self, user_id):
        return "questionnaire-data" in session

    def delete(self, user_id):
        del session[user_id]

    def clear(self):
        session.clear()

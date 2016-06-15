from flask import session
from app.storage.abstract_server_storage import AbstractServerStorage

QUESTIONNAIRE_DATA = "questionnaire-data"


class FlaskSessionStore(AbstractServerStorage):
    '''
    Client side storage using sessions
    '''

    def store(self, data, user_id, user_ik=None):
        session[QUESTIONNAIRE_DATA] = data

    def get(self, user_id, user_ik=None):
        if self.has_data(user_id):
            return session[QUESTIONNAIRE_DATA]
        else:
            return None

    def has_data(self, user_id):
        return QUESTIONNAIRE_DATA in session

    def delete(self, user_id):
        if self.has_data(user_id):
            del session[QUESTIONNAIRE_DATA]

    def clear(self):
        session.delete()

import logging

from app import settings
from app.authentication.user import QuestionnaireData

from flask_login import current_user

import jsonpickle

logger = logging.getLogger(__name__)

STATE = "state"


class StateManager(object):
    '''
    This class is responsible for saving the state of the User Journey Manager into the database.
    It does this by pickling the Python object graph into JSON and storing that. This means that code
    changes between deployments can cause odd behaviour if the database isn't wipe, as when it deserializes
    state from old python code to new python code attributes can be missing. Hence why we have the StateRecovery class
    '''
    @staticmethod
    def has_state():
        if settings.EQ_SERVER_SIDE_STORAGE_TYPE == 'DATABASE':
            return DatabaseStateManager.has_state()
        else:
            return InMemoryStateManager.has_state()

    @staticmethod
    def get_state():
        if settings.EQ_SERVER_SIDE_STORAGE_TYPE == 'DATABASE':
            return DatabaseStateManager.get_state()
        else:
            return InMemoryStateManager.get_state()

    @staticmethod
    def save_state(questionnaire_state):
        if settings.EQ_SERVER_SIDE_STORAGE_TYPE == 'DATABASE':
            DatabaseStateManager.save_state(questionnaire_state)
        else:
            InMemoryStateManager.save_state(questionnaire_state)

    @staticmethod
    def save_post_date(location, post_data):
        if settings.EQ_SERVER_SIDE_STORAGE_TYPE == 'DATABASE':
            DatabaseStateManager.save_post_date(location, post_data)
        else:
            InMemoryStateManager.save_post_date(location, post_data)


class InMemoryStateManager(StateManager):
    IN_MEMORY_STATE = {}

    @classmethod
    def has_state(cls):
        return bool(cls.IN_MEMORY_STATE)

    @classmethod
    def get_state(cls):
        return jsonpickle.decode(cls.IN_MEMORY_STATE)

    @classmethod
    def save_state(cls, questionnaire_state):
        cls.IN_MEMORY_STATE = jsonpickle.encode(questionnaire_state)


class DatabaseStateManager(StateManager):

    @staticmethod
    def has_state():
        data_query = QuestionnaireData(current_user.user_id, current_user.user_ik)
        questionnaire_data = data_query.data

        return STATE in questionnaire_data.keys()

    @staticmethod
    def get_state():
        data_query = QuestionnaireData(current_user.user_id, current_user.user_ik)
        questionnaire_data = data_query.data
        logger.debug("Returning questionnaire data %s", questionnaire_data)
        state = questionnaire_data[STATE]
        return jsonpickle.decode(state)

    @staticmethod
    def save_state(questionnaire_state):
        data_query = QuestionnaireData(current_user.user_id, current_user.user_ik)
        questionnaire_data = data_query.data
        questionnaire_data[STATE] = jsonpickle.encode(questionnaire_state)
        data_query.data = questionnaire_data
        data_query.save()

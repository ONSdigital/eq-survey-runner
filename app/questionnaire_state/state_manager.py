from flask_login import current_user
from app import settings
import jsonpickle
import logging

logger = logging.getLogger(__name__)

STATE = "state"


class StateManager(object):
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
        questionnaire_data = current_user.get_questionnaire_data()
        return STATE in questionnaire_data.keys()

    @staticmethod
    def get_state():
        questionnaire_data = current_user.get_questionnaire_data()
        logger.debug("Returning questionnaire data %s", questionnaire_data)
        state = questionnaire_data[STATE]
        return jsonpickle.decode(state)

    @staticmethod
    def save_state(questionnaire_state):
        questionnaire_data = current_user.get_questionnaire_data()
        questionnaire_data[STATE] = jsonpickle.encode(questionnaire_state)
        current_user.save()

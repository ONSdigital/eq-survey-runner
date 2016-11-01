import logging

from app import settings
from app.globals import get_questionnaire_store

from flask_login import current_user

import jsonpickle

logger = logging.getLogger(__name__)

USER_JOURNEY = "user_journey"


class UserJourneyManager(object):
    '''
    This class is responsible for saving the User Journey Manager into the database.
    It does this by pickling the Python object graph into JSON and storing that.
    '''
    @staticmethod
    def has_user_journey():
        if settings.EQ_SERVER_SIDE_STORAGE_TYPE == 'DATABASE':
            return DatabaseUserJourneyManager.has_user_journey()
        else:
            return InMemoryUserJourneyManager.has_user_journey()

    @staticmethod
    def get_user_journey():
        if settings.EQ_SERVER_SIDE_STORAGE_TYPE == 'DATABASE':
            return DatabaseUserJourneyManager.get_user_journey()
        else:
            return InMemoryUserJourneyManager.get_user_journey()

    @staticmethod
    def save_user_journey(user_journey):
        if settings.EQ_SERVER_SIDE_STORAGE_TYPE == 'DATABASE':
            DatabaseUserJourneyManager.save_user_journey(user_journey)
        else:
            InMemoryUserJourneyManager.save_user_journey(user_journey)

    @staticmethod
    def save_post_date(location, post_data):
        if settings.EQ_SERVER_SIDE_STORAGE_TYPE == 'DATABASE':
            DatabaseUserJourneyManager.save_post_date(location, post_data)
        else:
            InMemoryUserJourneyManager.save_post_date(location, post_data)


class InMemoryUserJourneyManager(UserJourneyManager):
    IN_MEMORY = {}

    @classmethod
    def has_user_journey(cls):
        return bool(cls.IN_MEMORY)

    @classmethod
    def get_user_journey(cls):
        return jsonpickle.decode(cls.IN_MEMORY)

    @classmethod
    def save_user_journey(cls, user_journey):
        cls.IN_MEMORY = jsonpickle.encode(user_journey)


class DatabaseUserJourneyManager(UserJourneyManager):

    @staticmethod
    def has_user_journey():
        store = get_questionnaire_store(current_user.user_id, current_user.user_ik)
        questionnaire_data = store.data

        return USER_JOURNEY in questionnaire_data.keys()

    @staticmethod
    def get_user_journey():
        store = get_questionnaire_store(current_user.user_id, current_user.user_ik)
        user_journey = store.data[USER_JOURNEY]
        logger.debug("Returning questionnaire user_journey %s", user_journey)
        return jsonpickle.decode(user_journey)

    @staticmethod
    def save_user_journey(user_journey):
        store = get_questionnaire_store(current_user.user_id, current_user.user_ik)
        store.data[USER_JOURNEY] = jsonpickle.encode(user_journey)
        store.save()

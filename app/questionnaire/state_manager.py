import logging

from app import settings

from flask_login import current_user

import jsonpickle

from werkzeug.datastructures import ImmutableMultiDict, MultiDict

logger = logging.getLogger(__name__)

STATE = "state"
POST_DATA = "post_data"


class StateManager(object):
    '''
    This class is responsible for saving the state of the User Journey Manager into the database.
    It does this by pickling the Python object graph into JSON and storing that. This means that code
    changes between deployments can cause odd behaviour if the database isn't wipe, as when it deserializes
    state from old python code to new python code attributes can be missing.
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
        questionnaire_data = current_user.get_questionnaire_data()
        # return STATE in questionnaire_data.keys()
        return POST_DATA in questionnaire_data.keys()

    @staticmethod
    def get_state():
        questionnaire_data = current_user.get_questionnaire_data()
        logger.debug("Returning questionnaire data %s", questionnaire_data)
        # TODO
        # state = questionnaire_data[STATE]
        # return jsonpickle.decode(state)

        return DatabaseStateManager.recover_from_post_data()

    @staticmethod
    def save_state(questionnaire_state):
        # questionnaire_data = current_user.get_questionnaire_data()
        # questionnaire_data[STATE] = jsonpickle.encode(questionnaire_state)
        # current_user.save()
        pass

    @staticmethod
    def save_post_date(location, post_data):
        logger.error("Saving Post Data %s", post_data)
        questionnaire_data = current_user.get_questionnaire_data()
        if POST_DATA not in questionnaire_data:
            questionnaire_data[POST_DATA] = []

        questionnaire_data[POST_DATA].append({'location': location, 'post_data': DatabaseStateManager._convert_to_dict(post_data)})
        current_user.save()

    @staticmethod
    def _convert_to_dict(post_data):
        logger.error("Multi dict is %s", post_data)
        return post_data.to_dict(flat=False)

    @staticmethod
    def recover_from_post_data():
        logger.debug("Recovering from post data")
        from app.questionnaire.questionnaire_manager import QuestionnaireManager
        from app.questionnaire.create_questionnaire_manager import get_schema

        logger.debug("Creating questionnaire manager")
        questionnaire_manager = QuestionnaireManager.new_instance(get_schema())

        logger.debug("Retrieving questionnaire data")
        questionnaire_data = current_user.get_questionnaire_data()
        if POST_DATA not in questionnaire_data:
            questionnaire_data[POST_DATA] = []

        all_post_data = questionnaire_data[POST_DATA]
        logger.debug("All post data %s", all_post_data)
        questionnaire_manager.go_to(questionnaire_manager.get_first_location())

        # basically this replays the post data in order
        for post_data in all_post_data:
            logger.debug("Replaying post data %s", post_data)
            location = post_data['location']
            data_to_replay = DatabaseStateManager._convert_to_multi_dict(post_data['post_data'])
            questionnaire_manager.go_to(location)
            location = questionnaire_manager.process_incoming_answers(location, data_to_replay, replay=True)
            logger.debug("Location %s", location)
        logger.debug("Post data replayed")

        return questionnaire_manager

    @staticmethod
    def _convert_to_multi_dict(post_data):
        multi_dict = MultiDict()
        for key in post_data.keys():
            for value in post_data[key]:
                multi_dict.add(key, value)

        logger.error("Recovered multi dict is %s", multi_dict)
        return ImmutableMultiDict(multi_dict)

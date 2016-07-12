from .navigation_state import NavigationContext
from abc import ABCMeta, abstractmethod
from flask_login import current_user

NAVIGATION_SESSION_KEY = "nav"


class INavigationStore(metaclass=ABCMeta):
    @abstractmethod
    def store_context(self, state):
        pass

    @abstractmethod
    def get_context(self):
        pass


class NavigationStore(INavigationStore):

    def __init__(self, schema):
        self._schema = schema

    def store_context(self, state):
        data = current_user.get_questionnaire_data()
        data[NAVIGATION_SESSION_KEY] = state.to_dict()

    def get_context(self):
        data = current_user.get_questionnaire_data()
        state = NavigationContext(self._schema)
        if NAVIGATION_SESSION_KEY in data:
            state.from_dict(data[NAVIGATION_SESSION_KEY])
        return state

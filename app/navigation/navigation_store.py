from .navigation_state import NavigationState
from abc import ABCMeta, abstractmethod
from flask_login import current_user

NAVIGATION_SESSION_KEY = "nav"


class INavigationStore(metaclass=ABCMeta):
    @abstractmethod
    def store_state(self, state):
        pass

    @abstractmethod
    def get_state(self):
        pass


class FlaskNavigationStore(INavigationStore):
    def store_state(self, state):
        data = current_user.get_questionnaire_data()
        data[NAVIGATION_SESSION_KEY] = state.to_dict()

    def get_state(self):
        data = current_user.get_questionnaire_data()
        state = NavigationState()
        if NAVIGATION_SESSION_KEY in data:
            state.from_dict(data[NAVIGATION_SESSION_KEY])
        return state

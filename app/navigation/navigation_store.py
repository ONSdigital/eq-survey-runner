from .navigation_state import NavigationState
from abc import ABCMeta, abstractmethod
from flask import session


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
        session[NAVIGATION_SESSION_KEY] = state.to_dict()
        session.permanent = True

    def get_state(self):
        state = NavigationState()
        if NAVIGATION_SESSION_KEY in session:
            state.from_dict(session[NAVIGATION_SESSION_KEY])
        return state

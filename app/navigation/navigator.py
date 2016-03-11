from abc import ABCMeta, abstractmethod
from flask import session, redirect
import json
import logging

NAVIGATION_SESSION_KEY = "nav"

logger = logging.getLogger(__name__)


class Navigator(object):
    def __init__(self, schema, navigation_history):
        self._schema = schema
        self._navigation_history = navigation_history
        self._store = NavigationStore()

    # destination  "group:block:section:question:<repetition>"
    def _valid_destination(self, destination):
        raise NotImplementedError()

    def get_current_location(self):
        state = self._store.get_state()

        if not state.started:
            return "start"
        if state.completed:
            return "completed"
        else:
            current_location = state.current_position
            logger.debug("Current location %s", current_location)
            raise current_location

    def go_to(self, location):
        if location == "start":
            return redirect("/cover-page")
        elif location == "completed":
            return redirect("/thank-you")
        else:
            return redirect("/questionnaire")


class NavigationState(object):
    def __init__(self):
        self.started = False
        self.current_position = None
        self.completed = False


class INavigationStore(metaclass=ABCMeta):
    @abstractmethod
    def store_state(self, state):
        pass

    @abstractmethod
    def get_state(self):
        pass


class NavigationStore(INavigationStore):
    def store_state(self, state):
        # TODO this doesn't work
        session[NAVIGATION_SESSION_KEY] = json.dumps(state)
        session.permanent = True

    def get_state(self):
        if NAVIGATION_SESSION_KEY in session:
            return json.loads(session[NAVIGATION_SESSION_KEY])
        else:
            return NavigationState()

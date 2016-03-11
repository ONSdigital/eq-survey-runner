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
        """
        Returns a boolean indicating whether a proposed destination is a valid one

        :param destination: The proposed destination

        :returns: True if valid, False otherwise

        """
        # TODO Addressable elements for navigation within a questionnaire need to be decided
        return True

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
        """
        Checks the validity of the proposed location and if valid, stores the
        current position in the history before updating the current position
        :param location: the location to go to next
        """
        if self._valid_destination(location):
            state = self._store.get_state()
            self._navigation_history.add_history_entry(state.current_position)
            state.current_position = location
            self._store.store_state(state)


class NavigationState(object):
    def __init__(self):
        self.started = False
        self.current_position = None
        self.completed = False

    def to_dict(self):
        return {
            "started": self.started,
            "completed": self.completed,
            "current_position": self.current_position
        }

    def from_dict(self, values):
        self.started = values['started'] or False
        self.completed = values['completed'] or {}
        self.current_position = values['current_position'] or {}


class INavigationStore(metaclass=ABCMeta):
    @abstractmethod
    def store_state(self, state):
        pass

    @abstractmethod
    def get_state(self):
        pass


class NavigationStore(INavigationStore):
    def store_state(self, state):
        session[NAVIGATION_SESSION_KEY] = state.to_dict()
        session.permanent = True

    def get_state(self):
        state = NavigationState()
        if NAVIGATION_SESSION_KEY in session:
            state.from_dict(session[NAVIGATION_SESSION_KEY])
        return state

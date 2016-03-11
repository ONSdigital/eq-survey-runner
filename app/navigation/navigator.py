from .navigation_store import FlaskNavigationStore
import logging

logger = logging.getLogger(__name__)


class Navigator(object):
    def __init__(self, schema, navigation_history):
        self._schema = schema
        self._navigation_history = navigation_history
        self._store = FlaskNavigationStore()

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
        """
        Load navigation state from the session, from that state get the current location
        :return: the current location in the questionnaire
        """
        state = self._store.get_state()
        current_location = state.current_position
        logger.debug("Current location %s", current_location)
        return current_location

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
        else:
            logger.warning("Location %s is not valid", location)

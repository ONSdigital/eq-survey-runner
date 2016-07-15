import logging
from app.navigation.navigation_store import NavigationStore


logger = logging.getLogger(__name__)


class Navigator(object):
    def __init__(self, schema, metadata, navigation_history):
        self._schema = schema
        self._metadata = metadata
        self._navigation_history = navigation_history
        self._store = NavigationStore(schema)

    def get_current_location(self):
        """
        Load navigation state from the session, from that state get the current location
        :return: the current location in the questionnaire
        """
        context = self._store.get_context()
        current_location = context.state.get_location()
        logger.debug("get current location %s", current_location)
        return current_location

    def go_to(self, location):
        """
        Checks the validity of the proposed location and if valid, stores the
        current position in the history before updating the current position
        :param location: the location to go to next
        """
        context = self._store.get_context()
        self._navigation_history.add_history_entry(context.state.get_location())
        logger.debug("go_to %s", location)
        context.go_to(location)
        self._store.store_context(context)

    def get_first_block(self):
        return self._schema.groups[0].blocks[0].id

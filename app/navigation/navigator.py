from app.utilities.factory import factory
import logging
from app.model.block import Block


logger = logging.getLogger(__name__)


class NavigationException(Exception):
    pass


class Navigator(object):
    def __init__(self, schema, navigation_history):
        self._schema = schema
        self._navigation_history = navigation_history
        self._store = factory.create("navigation-store")

    # destination  "group:block:section:question:<repetition>"
    def _valid_destination(self, destination):
        """
        Returns a boolean indicating whether a proposed destination is a valid one

        :param destination: The proposed destination

        :returns: True if valid, False otherwise

        """
        if destination == 'introduction':
            # 'introduction' is only a valid destination if the schema contains one
            if self._schema.introduction is not None:
                return True
            else:
                return False

        if destination == 'summary':
            return True

        if destination == 'thank-you':
            return True

        item = self._schema.get_item_by_id(destination)
        if isinstance(item, Block):
            return True

        return False

    def get_current_location(self):
        """
        Load navigation state from the session, from that state get the current location
        :return: the current location in the questionnaire
        """
        state = self._store.get_state()
        current_location = state.current_position
        logger.debug("Current location %s", current_location)

        # Blocks are the navigable elements within a questionnaire
        if current_location is None:
            # If there is no introduction, go to the first block
            if self._schema.introduction is not None:
                return 'introduction'
            else:
                return self._schema.groups[0].blocks[0].id
        else:
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
            raise NavigationException('Invalid location: {}'.format(location))

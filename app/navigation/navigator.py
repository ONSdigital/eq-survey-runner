import logging
from app.navigation.navigation_state import IntroductionState, QuestionnaireState

logger = logging.getLogger(__name__)


class Navigator(object):
    def __init__(self, schema, navigation_store):
        self._schema = schema
        self._store = navigation_store
        if self._schema.introduction:
            self.state = IntroductionState(schema)
        else:
            self.state = QuestionnaireState(schema)

    def get_current_location(self):
        """
        Load navigation state from the session, from that state get the current location
        :return: the current location in the questionnaire
        """
        current_location = self.state.get_location()
        logger.debug("get current location %s", current_location)
        return current_location

    def go_to(self, location):
        """
        Checks the validity of the proposed location and if valid, stores the
        current position in the history before updating the current position
        :param location: the location to go to next
        """
        logger.debug("go_to %s", location)
        # start at the beginning of a questionnaire
        state = IntroductionState(self._schema)
        # go to the new destination, this will update the state of the context
        state.go_to(self, location)
        self._store.save_navigator(self)

    def get_first_block(self):
        return self._schema.groups[0].blocks[0].id

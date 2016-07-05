from app.utilities.factory import factory
from app.model.questionnaire import QuestionnaireException
import logging
from app.model.block import Block


logger = logging.getLogger(__name__)


class NavigationStep(object):
    def __init__(self):
        self.next_step = None

    def set_next_step(self, step):
        self.next_step = step

    def is_valid(self, destination):
        logger.error("Is valid destination %s", destination)
        valid = False
        if destination == self.get_destination():
            valid = True
        elif self.next_step:
            valid = self.next_step.is_valid(destination)
        logger.error("Is valid %s", valid)
        return valid

    def next_destination(self):
        destination = self.get_destination()
        if destination:
            return destination
        else:
            return self.next_step.next_destination()

    def get_destination(self):
        return None


class Introduction(NavigationStep):
    def __init__(self, schema):
        self._schema = schema

    def get_destination(self):
        logger.error("Introduction returning from get_destination - introduction")
        if self._schema.introduction:
            return "introduction"
        else:
            return None


class Summary(NavigationStep):
    def get_destination(self):
        logger.error("Summary returning from get_destination - summary")
        return "summary"


class ThankYou(NavigationStep):
    def get_destination(self):
        logger.error("Thank you returning from get_destination - thank you")
        return "thank-you"


class Page(NavigationStep):
    def __init__(self, schema):
        self._schema = schema

    def is_valid(self, destination):
        # override is_valid as page have special conditions
        logger.error("Page is valid destination %s", destination)
        try:
            item = self._schema.get_item_by_id(destination)
            if isinstance(item, Block):
                return True
        except QuestionnaireException:
            pass
        return super().is_valid(destination)

    def get_destination(self):
        # always return the first page
        return self._schema.groups[0].blocks[0].id


class NavigationException(Exception):
    pass


class Navigator(object):
    def __init__(self, schema, navigation_history):
        self._schema = schema
        self._navigation_history = navigation_history
        self._store = factory.create("navigation-store")
        self.route = self._build_route()

    def _build_route(self):
        introduction = Introduction(self._schema)
        page = Page(self._schema)
        summary = Summary()
        thank_you = ThankYou()
        introduction.next_step = page
        page.next_step = summary
        summary.next_step = thank_you
        return introduction

    # destination  "group:block:section:question:<repetition>"
    def _valid_destination(self, destination):
        """
        Returns a boolean indicating whether a proposed destination is a valid one

        :param destination: The proposed destination

        :returns: True if valid, False otherwise

        """
        return self.route.is_valid(destination)

    def get_current_location(self):
        """
        Load navigation state from the session, from that state get the current location
        :return: the current location in the questionnaire
        """
        state = self._store.get_state()
        current_location = state.current_position
        logger.debug("Current location %s", current_location)

        if current_location is None:
            return self.route.next_destination()
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

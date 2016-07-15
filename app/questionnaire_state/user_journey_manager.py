from app.schema.block import Block as SchemaBlock
from app.questionnaire_state.block import Block as StateBlock
from app.questionnaire_state.page import Page
from app.questionnaire_state.state_manager import StateManager
import logging


logger = logging.getLogger(__name__)

STATE = "state"


class UserJourneyManager(object):
    def __init__(self, schema):
        self._schema = schema
        self._current = None  # the latest page
        self._first = None  # the first page in the doubly linked list
        self._archive = []  # a list of completed or discarded pages

    @staticmethod
    def new_instance(schema):
        user_journey_manager = UserJourneyManager(schema)
        StateManager.save_state(user_journey_manager)
        logger.debug("Constructing new state")
        return user_journey_manager

    @staticmethod
    def get_instance():
        # TODO optimize here as the schema is pickled along with the state
        # meaning we won't need to pass it every time.
        if StateManager.has_state():
            logger.debug("StateManager loading state")
            return StateManager.get_state()
        else:
            return None

    def get_state(self, item_id):
        page = self._first
        while page and item_id != page.item_id:
            page = page.next_page
        return page

    def go_to_state(self, item_id):
        page = self.get_state(item_id)
        logger.debug("go to state %s", item_id)
        if page:
            logger.debug("truncating to page %s", item_id)
            if page.next_page:
                self._truncate(page.next_page)
            logger.debug("current item %s", item_id)
            StateManager.save_state(self)
        else:
            logger.debug("creating new state for %s", item_id)
            self._create_new_state(item_id)

    def _create_new_state(self, item_id):
        item = self._schema.get_item_by_id(item_id)
        logger.debug("Creating new state for %s", item_id)
        if isinstance(item, SchemaBlock):
            state = StateBlock.construct_state(item)
            page = Page(item_id, state)
            self._append(page)
            StateManager.save_state(self)
        else:
            raise TypeError("Can only handle blocks")
        logger.debug("current item id is %s", self._current.item_id)

    def update_state(self, item_id, user_input):
        item = self._schema.get_item_by_id(item_id)
        logger.error("Updating state for item %s", item.id)
        if isinstance(item, SchemaBlock):
            logger.debug("item id is %s", item_id)
            if item_id == self._current.item_id:
                state = self._current.page_state
                state.update_state(user_input)
                StateManager.save_state(self)
            else:
                raise ValueError("Updating state for incorrect page")
        else:
            raise TypeError("Can only handle blocks")

    def _append(self, page):
        if not self._first:
            self._first = page
            self._current = page
        else:
            previous_page = self._current
            previous_page.next_page = page
            page.previous_page = previous_page
            self._current = page

    def _truncate(self, page):
        # truncate everything after page and archive it
        while page != self._current:
            self._archive.append(self._pop())
        # finally pop that page
        self._archive.append(self._pop())

    def _pop(self):
        page = self._current
        self._current = page.previous_page
        if self._current:
            self._current.next_page = None
        page.previous_page = None
        return page

    def get_current_state(self):
        return self._current.page_state

    # TODO temporary memory to support answer stored
    def get_first(self):
        return self._first

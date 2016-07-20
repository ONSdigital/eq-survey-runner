from app.questionnaire_state.page import Page
from app.questionnaire_state.state_manager import StateManager
from app.questionnaire_state.introduction import Introduction as StateIntroduction
from app.questionnaire_state.thank_you import ThankYou as StateThankYou
from app.questionnaire_state.summary import Summary as StateSummary
import logging


logger = logging.getLogger(__name__)

STATE = "state"


class UserJourneyManager(object):
    '''
    This class represents a user journey through a survey. It models the request/response process of the web application
    using a doubly linked list. Each node in the list is essentially a page displayed to the user. A new page is created
    by a GET request and subsequently updated via a POST request.

    The doubly linked list approach allows us to maintain the path the user has taken through the question. If that path
    changes we archive off the pages incase the user revists that path.

    '''
    def __init__(self, schema):
        self.submitted_at = None
        self._schema = schema
        self._current = None  # the latest page
        self._first = None  # the first page in the doubly linked list
        self._archive = []  # a list of completed or discarded pages
        self._valid_locations = self._build_valid_locations()

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

    def _build_valid_locations(self):
        validate_location = ['thank-you', 'summary']
        if self._schema.introduction:
            validate_location.append('introduction')
        for group in self._schema.children:
            for block in group.children:
                validate_location.append(block.id)
        return validate_location

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

        logger.debug("Creating new state for %s", item_id)
        if item_id in self._valid_locations:
            if item_id == 'introduction':
                state = StateIntroduction(item_id)
            elif item_id == 'thank-you':
                state = StateThankYou(item_id)
            elif item_id == 'summary':
                state = StateSummary(item_id)
            else:
                item = self._schema.get_item_by_id(item_id)
                state = item.construct_state()
            page = Page(item_id, state)
            self._append(page)
            StateManager.save_state(self)
        else:
            raise ValueError("Unsupported location %s", item_id)
        logger.debug("current item id is %s", self._current.item_id)

    def update_state(self, item_id, user_input):
        logger.error("Updating state for item %s", item_id)
        if item_id in self._valid_locations:
            logger.debug("item id is %s", item_id)
            logger.error("Current location %s", self.get_current_location())
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

    def get_current_location(self):
        if self._current:
            current_location = self._current.item_id
        else:
            current_location = self._get_first_location()
        logger.debug("get current location returning %s", current_location)
        return current_location

    def _get_first_location(self):
        if self._schema.introduction:
            return "introduction"
        else:
            return self._schema.groups[0].blocks[0].id

    # TODO temporary methods to support the template pre-processor
    def get_answers(self):

        # walk the list and collect all the answers
        answers_dict = {}

        page = self._first
        answers = []
        while page:
            page_answers = page.page_state.get_answers()
            answers.extend(page_answers)
            page = page.next_page

        for answer in answers:
            answers_dict[answer.id] = answer.input
        return answers_dict

    def get_answer(self, id):
        answers = self.get_answers()
        if id in answers:
            return answers[id]
        else:
            return None

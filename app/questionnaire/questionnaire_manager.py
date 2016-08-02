from app.questionnaire.state_manager import StateManager
from app.questionnaire_state.introduction import Introduction as StateIntroduction
from app.questionnaire_state.page import Page
from app.questionnaire_state.summary import Summary as StateSummary
from app.questionnaire_state.thank_you import ThankYou as StateThankYou
from app.schema.questionnaire import QuestionnaireException
from app.metadata.metadata_store import MetaDataStore
from app.templating.template_pre_processor import TemplatePreProcessor
from app.routing.routing_engine import RoutingEngine
from app.questionnaire.user_action_processor import UserActionProcessor
from app.authentication.session_management import session_manager
from flask_login import current_user
import logging
import bleach


logger = logging.getLogger(__name__)


class QuestionnaireManager(object):
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
        self._archive = {}  # a dict of completed or discarded pages
        self._valid_locations = self._build_valid_locations()
        self._pre_processor = TemplatePreProcessor(self._schema, self)

    @staticmethod
    def new_instance(schema):
        user_journey_manager = QuestionnaireManager(schema)
        # immediately save it to the database
        StateManager.save_state(user_journey_manager)
        logger.debug("Constructing new state")
        return user_journey_manager

    @staticmethod
    def get_instance():
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
        # traverse the list and find the state matching this item id
        page = self._first
        while page and item_id != page.item_id:
            page = page.next_page
        return page

    def is_valid_location(self, location):
        return location in self._valid_locations

    def go_to_state(self, item_id):
        page = self.get_state(item_id)
        logger.debug("go to state %s", item_id)
        if page:
            logger.debug("truncating to page %s", item_id)
            if page.next_page:
                self._truncate(page.next_page)
            logger.debug("current item %s", item_id)
            StateManager.save_state(self)
        elif item_id in self._archive:
            # re-append the old page to the head of the list
            self._append(self._archive[item_id])
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
            logger.debug("Current location %s", self.get_current_location())
            if item_id == self._current.item_id:
                state = self._current.page_state
                schema_item = None
                try:
                    schema_item = self._schema.get_item_by_id(item_id)
                except QuestionnaireException:
                    pass
                state.update_state(user_input, schema_item)
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
        logger.debug("Truncate everything after %s", page.item_id)
        logger.debug("Current position %s", self._current.item_id)
        # truncate everything after page and archive it
        while page != self._current:
            popped_page = self._pop()
            logger.debug("Archiving %s", popped_page.item_id)
            self._archive[popped_page.item_id] = popped_page
        # finally pop that page
        self._archive[page.item_id] = self._pop()
        logger.debug("Finally archiving %s", page.item_id)

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
            return self._get_first_block()

    def _get_first_block(self):
        return self._schema.groups[0].blocks[0].id

    def get_answers(self):
        '''
        This method walks the entire list collecting all answers and as such should
        only be used for the summary page and submission of data. Otherwise use the
        more efficient find_answer(id) method
        :return:
        '''

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

    def find_answer(self, id):
        # TODO we need to make this more efficient
        # The item class really should hold a dict of answer so we have quick lookups
        answers = self.get_answers()
        if id in answers:
            return answers[id]
        else:
            return None

    def validate(self):
        # get the current location in the questionnaire
        current_location = self.get_current_location()
        if self.is_valid_location(current_location):
            current_state = self.get_state(current_location)
            if self._schema.item_exists(current_state.item_id):
                schema_item = self._schema.get_item_by_id(current_state.item_id)

                return schema_item.validate(current_state.page_state)
            else:
                # Item has state, but is not in schema: must be introduction, thank you or summary
                return True
        else:
            # Not a validation location, so can't be valid
            return False

    @property
    def submitted(self):
        return self.submitted_at is not None

    def go_to(self, location):
        if location == 'first':
            # convenience method for routing to the first block
            location = self._get_first_block()
        self.go_to_state(location)
        self._pre_processor.initialize(MetaDataStore.get_instance(current_user))

    def process_incoming_answers(self, location, post_data):
        # ensure we're in the correct location
        self.go_to_state(location)

        # process incoming post data
        user_action, user_answers = self._process_incoming_post_data(post_data)

        # Process the answers and see where to go next
        cleaned_user_answers = {}
        for key, value in user_answers.items():
            cleaned_user_answers[key] = self._clean_input(value)

        # updated state
        self.update_state(location, user_answers)

        # get the current location in the questionnaire
        current_location = self.get_current_location()

        # run the validator to update the validation_store
        if self.validate():

            # process the user action
            user_action_processor = UserActionProcessor(self._schema, self)
            user_action_processor.process_action(user_action)

            # Create the routing engine
            routing_engine = RoutingEngine(self._schema, self)

            # do any routing
            next_location = routing_engine.get_next_location(current_location)
            logger.info("next location after routing is %s", next_location)

            # go to that location
            self.go_to_state(next_location)
            logger.debug("Going to location %s", next_location)
        else:
            # bug fix for using back button which then fails validation
            self.go_to_state(current_location)

        self._pre_processor.initialize(MetaDataStore.get_instance(current_user))
        # now return the location
        return self.get_current_location()

    def get_rendering_context(self):
        return self._pre_processor.build_view_data()

    def get_rendering_template(self):
        return self._pre_processor.get_template_name()

    def _process_incoming_post_data(self, post_data):
        user_answers = {}
        user_action = None

        for key in post_data.keys():
            if key.startswith('action['):
                # capture the required action
                user_action = key[7:-1]
            elif key.endswith('[]'):
                # is an array of Checkboxes
                answer_id = key[:-2]
                if answer_id not in user_answers.keys():
                    # copies the whole array
                    user_answers[answer_id] = post_data.getlist(key)
            else:
                # for now assume it is a valid answer id
                user_answers[key] = post_data[key]

        return user_action, user_answers

    def _clean_input(self, value):
        if isinstance(value, list):
            return value

        if value:
            whitespace_removed = value.strip()
            return bleach.clean(whitespace_removed)
        else:
            return value

    def delete_user_data(self):
        # once the survey has been submitted
        # delete all user data from the database
        current_user.delete_questionnaire_data()
        # and clear out the session state
        session_manager.clear()

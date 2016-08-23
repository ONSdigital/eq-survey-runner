import logging

from app.authentication.session_management import session_manager
from app.metadata.metadata_store import MetaDataStore
from app.piping.plumbing_preprocessor import PlumbingPreprocessor
from app.questionnaire.state_manager import StateManager
from app.questionnaire.user_action_processor import UserActionProcessor, UserActionProcessorException
from app.questionnaire_state.confirmation import Confirmation as StateConfirmation
from app.questionnaire_state.introduction import Introduction as StateIntroduction
from app.questionnaire_state.node import Node
from app.questionnaire_state.summary import Summary as StateSummary
from app.questionnaire_state.thank_you import ThankYou as StateThankYou

from app.routing.conditional_display import ConditionalDisplay
from app.routing.routing_engine import RoutingEngine
from app.templating.template_register import TemplateRegistry

from flask_login import current_user

logger = logging.getLogger(__name__)


class InvalidLocationException(Exception):
    pass


class QuestionnaireManager(object):
    '''
    This class represents a user journey through a survey. It models the request/response process of the web application
    using a doubly linked list. Each node in the list is essentially a page displayed to the user. A new node is created
    by a GET request and subsequently updated via a POST request.
    The doubly linked list approach allows us to maintain the path the user has taken through the question. If that path
    changes we archive off the nodes in case the user revisits that path.
    '''
    def __init__(self, schema):
        self.submitted_at = None
        self._schema = schema
        self._current = None  # the latest node
        self._first = None  # the first node in the doubly linked list
        self._tail = None
        self._archive = {}  # a dict of discarded nodes for later use (if needed)
        self._valid_locations = self._build_valid_locations()

    @staticmethod
    def new_instance(schema):
        questionnaire_manager = QuestionnaireManager(schema)
        # immediately save it to the database
        StateManager.save_state(questionnaire_manager)
        logger.debug("Constructing new state")
        return questionnaire_manager

    @staticmethod
    def get_instance():
        if StateManager.has_state():
            logger.debug("StateManager loading state")
            return StateManager.get_state()
        else:
            return None

    def resolve_location(self, location):
        if location == 'first':
            return self._get_first_block()
        elif location == 'previous':
            return self._current.previous.item_id
        else:
            return location

    def _build_valid_locations(self):
        validate_location = ['thank-you']

        # Add the submission page (default is summary)
        validate_location.append(self._schema.submission_page)

        if self._schema.introduction:
            validate_location.append('introduction')
        for group in self._schema.children:
            for block in group.children:
                validate_location.append(block.id)
        return validate_location

    def get_state(self, item_id):
        # traverse the list and find the state matching this item id
        node = self._first
        while node and item_id != node.item_id:
            node = node.next
        return node

    def is_valid_location(self, location):
        return location in self._valid_locations

    def go_to_state(self, item_id):
        node = self.get_state(item_id)
        logger.debug("go to state %s", item_id)
        if node:
            self._current = node
            logger.debug("current item %s", item_id)
        elif item_id in self._archive:
            # re-append the old node to the head of the list
            self._append(self._archive[item_id])
        else:
            logger.debug("creating new state for %s", item_id)
            self._create_new_state(item_id)
        StateManager.save_state(self)

    def _create_new_state(self, item_id):

        logger.debug("Creating new state for %s", item_id)
        if item_id in self._valid_locations:
            if item_id == 'introduction':
                state = StateIntroduction(item_id)
            elif item_id == 'thank-you':
                state = StateThankYou(item_id, self.submitted_at)
            elif item_id == 'summary':
                state = StateSummary(item_id)
            elif item_id == 'confirmation':
                state = StateConfirmation(item_id)
            else:
                item = self._schema.get_item_by_id(item_id)
                state = item.construct_state()
            node = Node(item_id, state)
            self._append(node)
        else:
            raise ValueError("Unsupported location %s", item_id)
        logger.debug("current item id is %s", self._current.item_id)

    def update_state(self, item_id, user_input):
        logger.debug("Updating state for item %s", item_id)
        if item_id in self._valid_locations:
            logger.debug("item id is %s", item_id)
            logger.debug("Current location %s", self.get_current_location())

            node = self.get_state(item_id)
            self._current = node
            state = node.state
            state.update_state(user_input)
            # Truncate following nodes
            if node.next:
                self._truncate(node.next)

            StateManager.save_state(self)
        else:
            raise TypeError("Can only handle blocks")

    def _append(self, node):
        if not self._first:
            self._first = node
            self._current = node
            self._tail = node
        else:
            previous = self._current
            previous.next = node
            node.previous = previous
            self._current = node
            self._tail = node

    def _truncate(self, node):
        logger.debug("Truncate everything after %s", node.item_id)
        logger.debug("Current position %s", self._current.item_id)
        # truncate everything after node and archive it
        while node != self._tail:
            popped_node = self._pop()
            logger.debug("Archiving %s", popped_node.item_id)
            self._archive[popped_node.item_id] = popped_node
        # finally pop that node
        self._archive[node.item_id] = self._pop()
        logger.debug("Finally archiving %s", node.item_id)

    def _pop(self):
        node = self._tail
        self._tail = node.previous
        if self._tail:
            self._tail.next = None
        node.previous = None
        return node

    def get_current_state(self):
        return self._current.state

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

    def _previous(self):
        return self._current.previous.item_id

    def get_answers(self):
        '''
        This method walks the entire list collecting all answers and as such should
        only be used for the summary node and submission of data. Otherwise use the
        more efficient find_answer(id) method
        :return:
        '''

        # walk the list and collect all the answers
        answers_dict = {}

        node = self._first
        answers = []
        while node:
            node_answers = node.state.get_answers()
            answers.extend(node_answers)
            node = node.next

        for answer in answers:
            answers_dict[answer.id] = answer.value
        return answers_dict

    def find_answer(self, id):
        # walk backwards through the list and check each block for the answer
        node = self._current
        while node:
            if id in node.state.answer_store:
                return node.state.answer_store[id]
            else:
                node = node.previous

    def validate(self):
        # get the current location in the questionnaire
        current_location = self.get_current_location()
        if self.is_valid_location(current_location):
            current_state = self.get_state(current_location)
            if self._schema.item_exists(current_state.item_id):
                schema_item = self._schema.get_item_by_id(current_state.item_id)

                return schema_item.validate(current_state.state)
            else:
                # Item has state, but is not in schema: must be introduction, thank you or summary
                return True
        else:
            # Not a validation location, so can't be valid
            return False

    def validate_all_answers(self):
        node = self._first
        valid = True
        while node:
            schema_item = node.state.schema_item
            if self._schema.item_exists(node.item_id):
                valid = schema_item.validate(node.state)
                if not valid:
                    current_location = node.item_id
                    logger.debug("Failed validation with current location %s", current_location)
                    # if one of the blocks isn't valid
                    # then move the current pointer to that block so that the user is redirected to that page
                    self.go_to_state(current_location)
                    break

                logger.debug("Next node is %s", node.item_id)

            node = node.next
        return valid

    @property
    def submitted(self):
        return self.submitted_at is not None

    def go_to(self, location):
        if self._current:
            logger.debug("Attempting to go to location %s with current location as %s", location, self._current.item_id)
        if location == 'first':
            # convenience method for routing to the first block
            location = self._get_first_block()
        elif location == 'previous':
            location = self._previous()
        elif location == 'summary' and self._current.item_id != 'summary':
            metadata = MetaDataStore.get_instance(current_user)
            if metadata:
                logger.warning("User with tx_id %s tried to submit in an invalid state", metadata.tx_id)
            raise InvalidLocationException()
        self.go_to_state(location)

    def is_known_state(self, location):
        if self._tail.item_id == location:
            return True
        node = self._tail
        while node.previous:
            if node.item_id == location:
                return True
            node = node.previous
        return False

    def process_incoming_answers(self, location, post_data):
        logger.debug("Processing post data for %s", location)
        # ensure we're in the correct location
        if self.is_known_state(location):
            self.go_to_state(location)

            # apply any conditional display rules
            self._conditional_display(self._current.state)

            # process incoming post data
            user_action = self._get_user_action(post_data)

            # updated state
            self.update_state(location, post_data)

            # run the validator to update the validation_store
            if self.validate():

                # process the user action
                try:
                    user_action_processor = UserActionProcessor(self._schema, self)
                    user_action_processor.process_action(user_action)

                    # Create the routing engine
                    routing_engine = RoutingEngine(self._schema, self)

                    # do any routing
                    next_location = routing_engine.get_next_location(location)
                    logger.info("next location after routing is %s", next_location)

                    # go to that location
                    self.go_to_state(next_location)
                    logger.debug("Going to location %s", next_location)
                except UserActionProcessorException as e:
                    logger.error("Error processing user actions")
                    logger.exception(e)
            else:
                # bug fix for using back button which then fails validation
                self.go_to_state(self.get_current_location())

            # now return the location
            current_location = self.get_current_location()
            logger.debug("Returning location %s", current_location)
            return current_location
        else:
            raise InvalidLocationException()

    def get_rendering_context(self, location):

        # apply any conditional display rules
        self._conditional_display(self.get_state(location).state)

        # look up the preprocessor and then build the view data
        preprocessor = TemplateRegistry.get_template_preprocessor(location)

        if location == 'summary':
            # the summary is the special case when we need the start of the linked list
            node = self._first
            # and we also need to plumb the entire schema
            while node.next:
                self._plumbing_preprocessing(node)
                node = node.next

            # reset pointer back to the first node for the preprocessor
            node = self._first

        else:
            # unlike the rest where we need the current node in the list
            node = self.get_state(location)
            # and only need to plumb the single page
            self._plumbing_preprocessing(node)
        return preprocessor.build_view_data(node, self._schema)

    def _plumbing_preprocessing(self, node):
        '''
        Run the current state through the plumbing preprocessor
        :return:
        '''
        plumbing_template_preprocessor = PlumbingPreprocessor()
        plumbing_template_preprocessor.plumb_current_state(self, node.state, self._schema)

    def _conditional_display(self, item):
        '''
        Process any conditional display rules
        :return:
        '''
        if item.schema_item:
            item.skipped = ConditionalDisplay.is_skipped(item.schema_item, self)
            for child in item.children:
                self._conditional_display(child)

    def get_rendering_template(self, location):
        return TemplateRegistry.get_template_name(location)

    def _get_user_action(self, post_data):
        user_action = None

        for key in post_data.keys():
            if key.startswith('action['):
                # capture the required action
                user_action = key[7:-1]

        return user_action

    def delete_user_data(self):
        # once the survey has been submitted
        # delete all user data from the database
        current_user.delete_questionnaire_data()
        # and clear out the session state
        session_manager.clear()

    def register_element_in_schema(self, item):
        self._schema.register(item)

    def check_item_exists_in_schema(self, item_id):
        return self._schema.item_exists(item_id)

    def get_schema_item_by_id(self, item_id):
        return self._schema.get_item_by_id(item_id)

    def add_repeating_element(self, item):
        self._schema.register(item)
        self._valid_locations.append(item.id)
        self._create_new_state(item.id)

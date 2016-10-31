import logging
import copy

from app.data_model.questionnaire_store import get_metadata
from app.piping.plumbing_preprocessor import PlumbingPreprocessor
from app.questionnaire.user_action_processor import UserActionProcessor, UserActionProcessorException
from app.questionnaire.user_journey import UserJourney
from app.questionnaire.user_journey_manager import UserJourneyManager
from app.questionnaire_state.node import Node

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
    using a doubly linked list. Each node in the list is a reference to a schema item and the answer the user has entered.
    A new node is created by a GET request and subsequently updated via a POST request.
    The doubly linked list approach allows us to maintain the path the user has taken through the question. If that path
    changes we archive off the nodes in case the user revisits that path.
    '''
    def __init__(self, schema, current=None, first=None, tail=None, archive=None, valid_locations=None, submitted_at=None):
        self.submitted_at = submitted_at
        self._schema = schema
        self._current = current  # the latest node
        self._first = first  # the first node in the doubly linked list
        self._tail = tail  # the last node in the doubly linked list
        self._archive = archive or {}  # a dict of discarded nodes for later use (if needed)
        self.state = None

        if valid_locations:
            self._valid_locations = valid_locations
        else:
            self._valid_locations = self._build_valid_locations()

    def construct_user_journey(self):
        return UserJourney(self._current, self._first, self._tail, self._archive, self.submitted_at, self._valid_locations)

    def _build_valid_locations(self):
        # Add the submission page (default is summary)
        validate_location = ['thank-you', self._schema.submission_page]

        if self._schema.introduction:
            validate_location.append('introduction')
        for group in self._schema.children:
            for block in group.children:
                validate_location.append(block.id)
        return validate_location

    def get_node(self, item_id):
        # traverse the list and find the node matching this item id
        node = self._first
        while node and item_id != node.item_id:
            node = node.next
        return node

    def go_to_node(self, item_id):
        node = self.get_node(item_id)
        logger.debug("go to node %s", item_id)
        if node:
            self._current = node
            logger.debug("current item %s", item_id)
        elif item_id in self._archive:
            # re-append the old node to the head of the list
            self._append(self._archive[item_id])
        else:
            logger.debug("creating new node for %s", item_id)
            self._create_new_node(item_id)
        UserJourneyManager.save_user_journey(self.construct_user_journey())

    def _create_new_node(self, item_id):
        node = Node(item_id)
        self._append(node)

    def update_node(self, item_id, user_input):
        logger.debug("Updating node for item %s", item_id)
        if item_id in self._valid_locations:
            logger.debug("item id is %s", item_id)
            logger.debug("Current location %s", self.get_current_location())
            node = self._current
            self._current = node

            # Truncate following nodes
            if node.next:
                self._truncate(node.next)
            UserJourneyManager.save_user_journey(self.construct_user_journey())
        else:
            raise TypeError("Can only handle blocks")

    def _append(self, node):
        if not self._first:
            self._first = node
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

    def get_current_location(self):
        if self._current:
            current_location = self._current.item_id
        else:
            current_location = self.get_first_location()
        logger.debug("get current location returning %s", current_location)
        return current_location

    def get_first_location(self):
        if self._schema.introduction:
            return "introduction"
        else:
            return self._get_first_block()

    def get_previous_location(self):
        return self._current.previous.item_id

    def _get_first_block(self):
        return self._schema.groups[0].blocks[0].id

    def get_answers(self):
        # walk the list and collect all the answers
        answers_dict = {}
        node = self._first

        while node:
            answers_dict.update(node.answers)
            node = node.next
        return answers_dict

    def find_answer(self, id):
        # walk backwards through the list and check each block for the answer
        node = self._current
        while node:
            if id in node.answers:
                return node.answers[id]
            else:
                node = node.previous

    def validate(self, post_data):
        # get the current location in the questionnaire
        current_location = self.get_current_location()
        if current_location in self._valid_locations:

            node = self._current
            self.build_state(node, post_data)

            if self.state:
                self._conditional_display(self.state)
                is_valid = self.state.schema_item.validate(self.state)
                # Todo, this doesn't feel right, validation is casting the user values to their type.
                # Save the answers to the node after validation
                self.update_node_answers(node)
                return is_valid

            else:
                # Item has node, but is not in schema: must be introduction, thank you or summary
                return True
        else:
            # Not a validation location, so can't be valid
            return False

    def update_node_answers(self, node):
        answer_dict = {}
        for answer in self.state.get_answers():
            answer_value = answer.other if answer.value == 'other' and answer.other else answer.value
            answer_dict[answer.id] = answer_value
        node.answers = answer_dict

    def validate_all_answers(self):
        node = self._first
        valid = True

        while node:
            self.build_state(node, node.answers)
            if self.state:
                self._conditional_display(self.state)
                is_valid = self.state.schema_item.validate(self.state)
                if not is_valid:
                    location = node.item_id
                    logger.debug("Failed validation with current location %s", location)
                    # if one of the blocks isn't valid
                    # then move the current pointer to that block so that the user is redirected to that page
                    self.go_to_node(location)
                    break

                logger.debug("Next node is %s", node.item_id)

            node = node.next
        return valid

    def go_to(self, location):
        if self._current:
            logger.debug("Attempting to go to location %s with current location as %s", location, self._current.item_id)
        if location == 'previous':
            location = self.get_previous_location()
        elif location == 'summary' and self._current.item_id != 'summary':
            metadata = get_metadata(current_user)
            if metadata:
                logger.warning("User with tx_id %s tried to submit in an invalid state", metadata["tx_id"])
            raise InvalidLocationException()
        self.go_to_node(location)

    def is_known_node(self, location):
        node = self._tail
        while node:
            if node.item_id == location:
                return True
            node = node.previous
        return False

    def process_incoming_answers(self, location, post_data, replay=False):
        logger.debug("QuestionnaireManager first %s", self._first)
        logger.debug("QuestionnaireManager current %s", self._current)
        logger.debug("QuestionnaireManager tail %s", self._tail)
        logger.debug("Processing post data for %s", location)
        # ensure we're in the correct location

        if self.is_known_node(location):
            self.go_to_node(location)

            # process incoming post data
            user_action = self._get_user_action(post_data)

            # updated node
            self.update_node(location, post_data)
            is_valid = self.validate(post_data)
            # run the validator to update the validation_store
            if is_valid:

                # process the user action
                try:
                    user_action_processor = UserActionProcessor(self._schema, self)
                    user_action_processor.process_action(user_action)

                    # Create the routing engine
                    routing_engine = RoutingEngine(self._schema, self)

                    # do any routing
                    next_location = routing_engine.get_next_location(location, user_action)
                    logger.info("next location after routing is %s", next_location)

                    # go to that location
                    self.go_to_node(next_location)
                    logger.debug("Going to location %s", next_location)
                except UserActionProcessorException as e:
                    logger.error("Error processing user actions")
                    logger.exception(e)
            else:
                # bug fix for using back button which then fails validation
                self.go_to_node(self.get_current_location())

            # now return the location
            current_location = self.get_current_location()
            logger.debug("Returning location %s", current_location)
            return is_valid
        else:
            raise InvalidLocationException()

    def get_rendering_context(self, location, is_valid=True):
        node = self._current
        state_items = []
        if is_valid:
            if location == 'summary':
                return self._get_summary_rendering_context()
            else:
                self.build_state(node, node.answers)

        if self.state:
            self._plumbing_preprocessing(self.state)
            self._conditional_display(self.state)

        if self.state not in state_items:
            state_items.append(self.state)

        # look up the preprocessor and then build the view data
        preprocessor = TemplateRegistry.get_template_preprocessor(location)
        return preprocessor.build_view_data(node, self._schema, state_items)

    def _get_summary_rendering_context(self):
        state_items = []
        # the summary is the special case when we need the start of the linked list
        node = self._first
        # We need to plumb the entire schema
        while node.next:
            self.build_state(node, node.answers)
            if self.state:
                self._plumbing_preprocessing(self.state)
                self._conditional_display(self.state)
                state_items.append(self.state)
            node = node.next

        # look up the preprocessor and then build the view data
        preprocessor = TemplateRegistry.get_template_preprocessor('summary')
        return preprocessor.build_view_data(node, self._schema, state_items)

    def build_state(self, node, answers):
        # Build the state from the linked list and the answers
        self.state = None
        if self._schema.item_exists(node.item_id):
            schema_item = self._schema.get_item_by_id(node.item_id)
            self.state = schema_item.construct_state()
            self.state.update_state(answers)

    def _plumbing_preprocessing(self, state):
        # Run the current state through the plumbing preprocessor
        plumbing_template_preprocessor = PlumbingPreprocessor()
        plumbing_template_preprocessor.plumb_current_state(self, self.state, self._schema)

    def _conditional_display(self, item):
        # Process any conditional display rules

        if item.schema_item:

            item.skipped = ConditionalDisplay.is_skipped(item.schema_item, self)
            for child in item.children:
                self._conditional_display(child)

    def _get_user_action(self, post_data):
        user_action = None

        for key in post_data.keys():
            if key.startswith('action['):
                # capture the required action
                user_action = key[7:-1]

        return user_action

    def get_schema_item_by_id(self, item_id):
        return self._schema.get_item_by_id(item_id)

    def add_household_answer(self):
        if self.state is None:
            return

        # TODO This probably needs to be moved somewhere else...
        # TODO Probably also need to guard for conditions like item not found etc...
        household_answer = self._schema.get_item_by_id('person')
        new_person_answer = household_answer.construct_state()

        household_question_schema = self._schema.get_item_by_id('household-question')
        household_question = self.state.find_state_item(household_question_schema)

        state_answers = household_question.children
        num_answers = len(state_answers)

        new_composite_answer = copy.deepcopy(new_person_answer.schema_item)
        new_composite_answer.widget.name += str(num_answers)

        new_person_answer.schema_item = new_composite_answer
        state_answers.append(new_person_answer)

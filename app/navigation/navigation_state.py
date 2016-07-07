from app.model.block import Block
from app.model.questionnaire import QuestionnaireException
import logging

logger = logging.getLogger(__name__)


class NavigationException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class NavigationState(object):
    '''
    Using a state pattern to keep track of the users position in the questionnaire
    '''
    def go_to(self, navigation_context, destination):
        logger.debug("Attempting to go to destination %s", destination)
        if destination == self.get_location():
            logger.debug("Already at destination %s", destination)
            navigation_context.state = self
        else:
            next_state = self.get_next_state()
            logger.debug("Going to next state %s", next_state.get_location())
            next_state.go_to(navigation_context, destination)

    def get_location(self):
        return None

    def get_next_state(self):
        return None


class IntroductionState(NavigationState):
    def __init__(self, schema):
        self._schema = schema

    def get_location(self):
        if self._schema.introduction:
            logger.debug("IntroductionState get_location - introduction")
            return "introduction"
        else:
            logger.debug("IntroductionState get_location - None")
            return None

    def get_next_state(self):
        return QuestionnaireState(self._schema)


class QuestionnaireState(NavigationState):
    def __init__(self, schema):
        self._schema = schema
        self.location = self._schema.groups[0].blocks[0].id

    def _is_valid(self, destination):
        logger.debug("Page is valid destination %s", destination)
        try:
            item = self._schema.get_item_by_id(destination)
            # if the item is a block we can navigate to it
            return isinstance(item, Block)
        except QuestionnaireException:
            logger.debug("Request destination is not valid in the schema %s", destination)
            return False

    def get_location(self):
        return self.location

    def go_to(self, navigation_context, destination):
        # questionnaire state is special as it can handle multiple destinations
        # e.g. different blocks in the schema
        if self._is_valid(destination):
            navigation_context.state = self
            self.location = destination
        else:
            super().go_to(navigation_context, destination)

    def get_next_state(self):
        return SummaryState()


class SummaryState(NavigationState):
    def get_location(self):
        return "summary"

    def get_next_state(self):
        return ThankYouState()


class ThankYouState(NavigationState):
    def get_location(self):
        return "thank-you"

    def get_next_state(self):
        # thank you state is the last state, if the destination doesn't match
        # then it is an invalid location
        raise NavigationException('Invalid location')


class NavigationContext(object):

    def __init__(self, schema):
        self._schema = schema
        if self._schema.introduction:
            self.state = IntroductionState(schema)
        else:
            self.state = QuestionnaireState(schema)

    def go_to(self, destination):
        # start at the beginning of a questionnaire
        state = IntroductionState(self._schema)
        # go to the new destination, this will update the state of the context
        state.go_to(self, destination)

    def to_dict(self):
        state = {
            "current_position": self.state.get_location()
        }
        logger.debug("NavigationContext to dict %s", state)
        return state

    def from_dict(self, values):
        current_location = values['current_position'] or None
        logger.debug("Attempting to go to position %s", current_location)
        self.go_to(destination=current_location)
        logger.debug("Navigation Context from dict %s", values)

import logging
from app.navigation.navigation_store import NavigationStore
from app.submitter.converter import SubmitterConstants
from app.utilities.factory import factory
from flask import session
from flask_login import current_user
from app.submitter.submitter import SubmitterFactory
from app import settings


logger = logging.getLogger(__name__)


class UserActionException(Exception):
    pass


class UserAction(object):
    '''
    Using the chain of responsibility pattern hand off a user action down the chain
    until one of the objects can handle it
    '''
    def __init__(self, schema, metadata):
        self._schema = schema
        self._metadata = metadata
        self.next_action = None

    def set_next_action(self, action):
        self.next_action = action
        return action

    def process_action(self, action, current_location):
        # work through the user actions to determine which one matches the request action
        if action == self.get_action():
            # perform any functionality necessary to complete that action
            self.perform_action()
            # then provide the next location
            return self.provide_next_location(current_location)
        else:
            # request the next location
            return self.next_action.process_action(action, current_location)

    def get_action(self):
        # subclasses should provide the name of the action it can support
        pass

    def perform_action(self):
        # subclasses should perform any functionality necessary to execute the user action
        pass

    def provide_next_location(self, current_location):
        # subclasses should prove the next location
        pass


class StartQuestionnaire(UserAction):
    def get_action(self):
        return 'start_questionnaire'

    def provide_next_location(self, current_location):
        return self._schema.groups[0].blocks[0].id


class SaveContinue(UserAction):
    def get_action(self):
        return 'save_continue'

    def provide_next_location(self, current_location):
        current_block = self._schema.get_item_by_id(current_location)
        if current_block:
            current_group = current_block.container

            for index, block in enumerate(current_group.blocks):
                if block.id == current_block.id:
                    if index + 1 < len(current_group.blocks):
                        # return the next block in this group
                        return current_group.blocks[index + 1].id
            for index, group in enumerate(self._schema.groups):
                if group.id == current_group.id:
                    if index + 1 < len(self._schema.groups):
                        # return the first block in the next group
                        return self._schema.groups[index + 1].blocks[0].id

            # There are no more blocks or groups, go to summary
            return 'summary'
        else:
            raise UserActionException('Cannot route: No current block')


class SubmitAnswers(UserAction):
    def get_action(self):
        return 'submit_answers'

    def provide_next_location(self, current_location):
        return 'thank-you'

    def perform_action(self):
        answer_store = factory.create("answer-store")
        answers = answer_store.get_answers()
        submitter = SubmitterFactory.get_submitter()
        submitted_at = submitter.send_answers(current_user, self._metadata, self._schema, answers)
        # TODO I don't like this but until we sort out the landing/review/submission flow this is the easiest way
        session[SubmitterConstants.SUBMITTED_AT_KEY] = submitted_at.strftime(settings.DISPLAY_DATETIME_FORMAT)
        return


class Navigator(object):
    def __init__(self, schema, metadata, navigation_history, routing_engine):
        self._schema = schema
        self._metadata = metadata
        self._navigation_history = navigation_history
        self._store = NavigationStore(schema)
        self._user_actions = self._build_user_action_chain()
        self._routing_engine = routing_engine

    def _build_user_action_chain(self):
        # builds the chain of responsibility
        start_questionnaire = StartQuestionnaire(self._schema, self._metadata)
        save_continue = SaveContinue(self._schema, self._metadata)
        submit = SubmitAnswers(self._schema, self._metadata)
        start_questionnaire.set_next_action(save_continue).set_next_action(submit)
        return start_questionnaire

    def get_current_location(self):
        """
        Load navigation state from the session, from that state get the current location
        :return: the current location in the questionnaire
        """
        context = self._store.get_context()
        current_location = context.state.get_location()
        logger.debug("get current location %s", current_location)
        return current_location

    def get_next_location(self, current_location, user_action):
        logging.debug("next location for %s and %s", current_location, user_action)
        # let the user action chain work out the next location
        next_location = self._user_actions.process_action(user_action, current_location)
        # then apply any routing rules
        next_location = self._routing_engine.get_next(next_location)
        logger.debug("next location %s", next_location)
        return next_location

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

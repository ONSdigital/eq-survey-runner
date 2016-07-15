from app.submitter.converter import SubmitterConstants
from app.utilities.factory import factory
from flask import session
from flask_login import current_user
from app.submitter.submitter import SubmitterFactory
from app import settings


class UserActionException(Exception):
    pass


class UserActionProcessor(object):

    def __init__(self, schema, metadata):
        self._schema = schema
        self._metadata = metadata
        self._user_actions = self._build_user_action_chain()

    def _build_user_action_chain(self):
        # builds the chain of responsibility
        start_questionnaire = StartQuestionnaire(self._schema, self._metadata)
        save_continue = SaveContinue(self._schema, self._metadata)
        submit = SubmitAnswers(self._schema, self._metadata)
        start_questionnaire.set_next_action(save_continue).set_next_action(submit)
        return start_questionnaire

    def process_action(self, action, current_location):
        return self._user_actions.process_action(action, current_location)


class UserAction(object):
    '''
    Using the chain of responsibility pattern hand off a user action down the chain
    until one of the objects can handle it
    '''
    def __init__(self, schema, metadata):
        self._schema = schema
        self._metadata = metadata
        self.next_action = None
        # subclasses should provide the name of the action it can support
        self.action = None

    def set_next_action(self, action):
        self.next_action = action
        return action

    def process_action(self, action, current_location):
        # work through the user actions to determine which one matches the request action
        if action == self.action:
            # perform any functionality necessary to complete that action
            self.perform_action()
            # then provide the next location
            return self.provide_next_location(current_location)
        else:
            # request the next location
            return self.next_action.process_action(action, current_location)

    def perform_action(self):
        # subclasses should perform any functionality necessary to execute the user action
        pass

    def provide_next_location(self, current_location):
        # subclasses should prove the next location
        pass


class StartQuestionnaire(UserAction):
    def __init__(self, schema, metadata):
        super().__init__(schema, metadata)
        self.action = 'start_questionnaire'

    def provide_next_location(self, current_location):
        return self._schema.groups[0].blocks[0].id


class SaveContinue(UserAction):
    def __init__(self, schema, metadata):
        super().__init__(schema, metadata)
        self.action = 'save_continue'

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
    def __init__(self, schema, metadata):
        super().__init__(schema, metadata)
        self.action = 'submit_answers'

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

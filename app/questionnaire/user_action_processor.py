import logging

from app import settings
from app.data_model.questionnaire_store import get_metadata
from app.submitter.submitter import SubmitterFactory

from flask_login import current_user

logger = logging.getLogger(__name__)


class UserActionProcessorException(Exception):
    pass


class UserActionProcessor(object):

    def __init__(self, schema, questionnaire_manager):
        self._schema = schema
        self._metadata = get_metadata(current_user)
        self._questionnaire_manager = questionnaire_manager
        self._user_actions = self._build_user_action_chain()

    def _build_user_action_chain(self):
        # builds the chain of responsibility
        start_questionnaire = StartQuestionnaire(self._schema, self._metadata)
        save_continue = SaveContinue(self._schema, self._metadata)
        submit = SubmitAnswers(self._schema, self._metadata, self._questionnaire_manager)
        start_questionnaire.set_next_action(save_continue).set_next_action(submit)
        return start_questionnaire

    def process_action(self, action):
        return self._user_actions.process_action(action)


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

    def process_action(self, action):
        # work through the user actions to determine which one matches the request action
        if action == self.action:
            # perform any functionality necessary to complete that action
            self.perform_action()
            # then provide the next location
        else:
            # request the next location
            self.next_action.process_action(action)

    def perform_action(self):
        # subclasses should perform any functionality necessary to execute the user action
        pass


class StartQuestionnaire(UserAction):
    def __init__(self, schema, metadata):
        super().__init__(schema, metadata)
        self.action = 'start_questionnaire'

    def perform_action(self):
        pass


class SaveContinue(UserAction):
    def __init__(self, schema, metadata):
        super().__init__(schema, metadata)
        self.action = 'save_continue'

    def perform_action(self):
        pass


class SubmitAnswers(UserAction):
    def __init__(self, schema, metadata, questionnaire_manager):
        super().__init__(schema, metadata)
        self.action = 'submit_answers'
        self._questionnaire_manager = questionnaire_manager

    def perform_action(self):
        answers = self._questionnaire_manager.get_answers()

        # check that all the answers we have are valid before submitting the data
        is_valid = self._questionnaire_manager.validate_all_answers()

        if is_valid:
            submitter = SubmitterFactory.get_submitter()
            submitted_at = submitter.send_answers(current_user, self._metadata, self._schema, answers)
            local_submitted_at = submitted_at.astimezone(settings.EUROPE_LONDON)
            logger.debug("setting submitted at %s", local_submitted_at)
            self._questionnaire_manager.submitted_at = local_submitted_at.strftime(settings.DISPLAY_DATETIME_FORMAT)
        else:
            raise UserActionProcessorException("Unable to submit - answers are not valid")

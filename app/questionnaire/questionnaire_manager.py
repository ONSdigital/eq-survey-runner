import bleach
from app.templating.template_pre_processor import TemplatePreProcessor
from app.submitter.converter import SubmitterConstants
from app.utilities.factory import factory
from flask import session
from flask_login import current_user
from app.submitter.submitter import SubmitterFactory
from app import settings

# TODO I really like this pattern however it is in the wrong place here.
# the navigator should deal with user action and it should call out to the
# routing engine to deal with any routing requirements  which current there
# aren't any so this component should simply do nothing.
# Therefore all this functionality needs to move to the navigator and then I
# think we combine and refactor that functionality


class QuestionnaireManagerException(Exception):
    pass


class UserAction(object):
    '''
    Using the chain of responsibility pattern hand off a user action down the chain
    until one of the objects can handle it
    '''
    def __init__(self, schema):
        self._schema = schema
        self.next_action = None

    def set_next_action(self, action):
        self.next_action = action
        return action

    def process_action(self, action, current_location):
        # work through the user actions to determine which one matches the request action
        if action == self.get_action():
            return self.provide_next_location(current_location)
        else:
            # perform any functionality necessary to complete that action
            self.perform_action()
            # request the next location
            return self.next_action.process_action(action, current_location)

    def get_action(self):
        pass

    def perform_action(self):
        pass

    def provide_next_location(self, current_location):
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
        # We have already been validated so we only
        # need to figure out where to go next
        next_location = current_location
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
            next_location = 'summary'
            return next_location
        else:
            raise QuestionnaireManagerException('Cannot route: No current block')


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


class QuestionnaireManager(object):
    def __init__(self, schema, answer_store, validator, validation_store, routing_engine, navigator, navigation_history, metadata):
        self._schema = schema
        self.answer_store = answer_store
        self._validator = validator
        self._validation_store = validation_store
        self._routing_engine = routing_engine
        self._navigator = navigator
        self._navigation_history = navigation_history
        self._metadata = metadata
        self.pre_processor = TemplatePreProcessor(self._schema, self.answer_store, self._validation_store, self._navigator, self._metadata)
        self.user_actions = self._build_user_action_chain()

    def _build_user_action_chain(self):
        # build the chain of responsibility
        start_questionnaire = StartQuestionnaire(self._schema)
        save_continue = SaveContinue(self._schema)
        submit = SubmitAnswers(self._schema)
        start_questionnaire.set_next_action(save_continue).set_next_action(submit)
        return start_questionnaire

    def get_next(self, current_location, user_action):
        return self.user_actions.process_action(user_action, current_location)

    def process_incoming_answers(self, post_data):
        # process incoming post data
        user_action, user_answers = self._process_incoming_post_data(post_data)

        # Process the answers and see where to go next
        cleaned_user_answers = {}
        for key, value in user_answers.items():
            cleaned_user_answers[key] = self._clean_input(value)

        # update the answer store with data
        for key, value in cleaned_user_answers.items():
            self.answer_store.store_answer(key, value)

        # get the current location in the questionnaire
        current_location = self._navigator.get_current_location()

        # run the validator to update the validation_store
        if self._validator.validate(cleaned_user_answers):

            # do any routing
            next_location = self.get_next(current_location, user_action)

            # go to that location
            self._navigator.go_to(next_location)
        else:
            # bug fix for using back button which then fails validation
            self._navigator.go_to(current_location)

        # now return the location
        return self._navigator.get_current_location()

    def get_rendering_context(self):
        return self.pre_processor.build_view_data()

    def get_rendering_template(self):
        return self.pre_processor.get_template_name()

    def _process_incoming_post_data(self, post_data):
        user_answers = {}
        user_action = None

        for key in post_data.keys():
            if key.endswith('-day'):
                # collect the matching -month, and -year fields and return a single answer for validation
                answer_id = key[0:-4]
                month_key = answer_id + '-month'
                year_key = answer_id + '-year'

                if month_key not in post_data.keys() or year_key not in post_data.keys():
                    continue

                # We do not validate here, only concatenate the inputs into a single answer which is validated elsewhere
                # we concatenate the fields into a date of the format dd/mm/yyyy
                user_answers[answer_id] = post_data[key] + '/' + post_data[month_key] + '/' + post_data[year_key]

            elif key.endswith('-month') or key.endswith('-year'):
                # skip theses, they are handled above
                continue
            elif key.startswith('action['):
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

    def get_current_location(self):
        return self._navigator.get_current_location()

    def go_to_location(self, location):
        self._navigator.go_to(location)

    def go_to_first(self):
        self._navigator.go_to(self._navigator.get_first_block())

    def get_schema(self):
        return self._schema

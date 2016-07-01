import bleach
from app.renderer.renderer import Renderer
from app.submitter.converter import SubmitterConstants
from flask import session
from flask_login import current_user
from app.submitter.submitter import SubmitterFactory
from app import settings


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

        self.renderer = Renderer(self._schema, self.answer_store, self._validation_store, self._navigator, self._metadata)

    def process_incoming_answers(self, post_data):
        # process incoming post data
        user_action, user_answers = self._process_incoming_post_data(post_data)

        # Are we submitting downstram?
        if user_action == 'submit_answers':
            return self.submit()

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
            next_location = self._routing_engine.get_next(current_location, user_action)

            # go to that location
            self._navigator.go_to(next_location)
        else:
            # bug fix for using back button which then fails validation
            self._navigator.go_to(current_location)

        # now return the location
        return self._navigator.get_current_location()

    def submit(self):
        answers = self.answer_store.get_answers()
        submitter = SubmitterFactory.get_submitter()
        submitted_at = submitter.send_answers(current_user, self._metadata, self._schema, answers)
        # TODO I don't like this but until we sort out the landing/review/submission flow this is the easiest way
        session[SubmitterConstants.SUBMITTED_AT_KEY] = submitted_at.strftime(settings.DISPLAY_DATETIME_FORMAT)
        self._navigator.go_to('thank-you')
        return

    def get_rendering_context(self):
        return self.renderer.render()

    def get_rendering_template(self):
        return self.renderer.get_template_name()

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

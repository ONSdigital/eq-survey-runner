import bleach
from app.renderer.renderer import Renderer
from app.submitter.converter import SubmitterConstants
from flask import session
from flask_login import current_user
from app.submitter.submitter import SubmitterFactory
from app import settings


class QuestionnaireManager(object):
    def __init__(self, schema, response_store, validator, validation_store, routing_engine, navigator, navigation_history, metadata):
        self._schema = schema
        self._response_store = response_store
        self._validator = validator
        self._validation_store = validation_store
        self._routing_engine = routing_engine
        self._navigator = navigator
        self._navigation_history = navigation_history
        self._metadata = metadata
        self.renderer = Renderer(self._schema, self._response_store, self._validation_store, self._navigator, self._metadata)

    def process_incoming_responses(self, post_data):
        # process incoming post data
        user_action, user_responses = self._process_incoming_post_data(post_data)

        # Are we submitting downstram?
        if user_action == 'submit_answers':
            responses = self._response_store.get_responses()
            submitter = SubmitterFactory.get_submitter()
            submitted_at = submitter.send_responses(current_user, self._metadata, self._schema, responses)
            # TODO I don't like this but until we sort out the landing/review/submission flow this is the easiest way
            session[SubmitterConstants.SUBMITTED_AT_KEY] = submitted_at.strftime(settings.DISPLAY_DATETIME_FORMAT)
            self._response_store.clear_responses()
            self._navigator.go_to('thank-you')
            return

        # Process the responses and see where to go next
        cleaned_user_responses = {}
        for key, value in user_responses.items():
            cleaned_user_responses[key] = self._clean_input(value)

        # update the response store with data
        for key, value in cleaned_user_responses.items():
            self._response_store.store_response(key, value)

        # get the current location in the questionnaire
        current_location = self._navigator.get_current_location()

        # run the validator to update the validation_store
        if self._validator.validate(cleaned_user_responses):

            # do any routing
            next_location = self._routing_engine.get_next(current_location, user_action)

            # go to that location
            self._navigator.go_to(next_location)
        else:
            # bug fix for using back button which then fails validation
            self._navigator.go_to(current_location)

        # now return the location
        return self._navigator.get_current_location()

    def get_rendering_context(self):
        return self.renderer.render()

    def get_rendering_template(self):
        return self.renderer.get_template_name()

    def _process_incoming_post_data(self, post_data):
        user_responses = {}
        user_action = None
        for key in post_data.keys():
            if key.endswith('-day'):
                # collect the matching -month, and -year fields and return a single response for validation
                response_id = key[0:-4]
                month_key = response_id + '-month'
                year_key = response_id + '-year'

                if month_key not in post_data.keys() or year_key not in post_data.keys():
                    continue

                # We do not validate here, only concatenate the inputs into a single response which is validated elsewhere
                # we concatenate the fields into a date of the format dd/mm/yyyy
                user_responses[response_id] = post_data[key] + '/' + post_data[month_key] + '/' + post_data[year_key]

            elif key.endswith('-month') or key.endswith('-year'):
                # skip theses, they are handled above
                continue
            elif key.startswith('action['):
                # capture the required action
                user_action = key[7:-1]
            else:
                # for now assume it is a valid response id
                user_responses[key] = post_data[key]

        return user_action, user_responses

    def _clean_input(self, value):
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

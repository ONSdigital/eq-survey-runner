import bleach
from app.templating.template_pre_processor import TemplatePreProcessor
from app.questionnaire_state.user_journey_manager import UserJourneyManager
from app.questionnaire.user_action_processor import UserActionProcessor
import logging


logger = logging.getLogger(__name__)


class QuestionnaireManager(object):
    def __init__(self, schema, answer_store, validator, validation_store, navigator, routing_engine, metadata):
        self._schema = schema
        self._user_journey_manager = UserJourneyManager.get_instance()
        if not self._user_journey_manager:
            self._user_journey_manager = UserJourneyManager.new_instance(self._schema)
        self._answer_store = answer_store
        self._validator = validator
        self._validation_store = validation_store
        self._navigator = navigator
        self._metadata = metadata
        self._routing_engine = routing_engine
        self._user_action_processor = UserActionProcessor(self._schema, self._metadata)

        # TODO lifecycle issue here - calling answer store before its ready
        self._pre_processor = TemplatePreProcessor(self._schema, self._answer_store, self._validation_store, self._navigator, self._metadata)

    def go_to_state(self, location):
        if self._schema.item_exists(location):
            self._user_journey_manager.go_to_state(location)

    def process_incoming_answers(self, location, post_data):
        # process incoming post data
        user_action, user_answers = self._process_incoming_post_data(post_data)

        # Process the answers and see where to go next
        cleaned_user_answers = {}
        for key, value in user_answers.items():
            cleaned_user_answers[key] = self._clean_input(value)

        if self._schema.item_exists(location):
            # updated state
            self._user_journey_manager.update_state(location, user_answers)

        # get the current location in the questionnaire
        current_location = self._navigator.get_current_location()

        # run the validator to update the validation_store
        if self._validator.validate(cleaned_user_answers):

            # process the user action
            next_location = self._user_action_processor.process_action(user_action, current_location)

            # do any routing
            next_location = self._routing_engine.get_next(next_location)
            logger.debug("next location after routing is %s", next_location)

            # go to that location
            self._navigator.go_to(next_location)
            logger.debug("Going to location %s", next_location)
        else:
            # bug fix for using back button which then fails validation
            self._navigator.go_to(current_location)

        # now return the location
        return self._navigator.get_current_location()

    def get_rendering_context(self):
        return self._pre_processor.build_view_data()

    def get_rendering_template(self):
        return self._pre_processor.get_template_name()

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

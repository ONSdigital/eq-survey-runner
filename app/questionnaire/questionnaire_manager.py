import bleach
from app.templating.template_pre_processor import TemplatePreProcessor

from app.questionnaire.user_action_processor import UserActionProcessor
from app.authentication.session_management import session_manager
from flask_login import current_user
import logging


logger = logging.getLogger(__name__)


class QuestionnaireManager(object):
    def __init__(self, schema, user_journey_manager, routing_engine, metadata):
        self._schema = schema
        self._user_journey_manager = user_journey_manager
        self._metadata = metadata
        self._routing_engine = routing_engine
        self._user_action_processor = UserActionProcessor(self._schema, self._metadata, self._user_journey_manager)
        self._pre_processor = TemplatePreProcessor(self._schema, self._user_journey_manager, self._metadata)

    @property
    def submitted(self):
        return self._user_journey_manager.submitted_at is not None

    def go_to(self, location):
        if location == 'first':
            # convenience method for routing to the first block
            location = self._routing_engine.get_first_block()
        self._user_journey_manager.go_to_state(location)
        self._pre_processor.initialize()

    def process_incoming_answers(self, location, post_data):
        # ensure we're in the correct location
        self._user_journey_manager.go_to_state(location)

        # process incoming post data
        user_action, user_answers = self._process_incoming_post_data(post_data)

        # Process the answers and see where to go next
        cleaned_user_answers = {}
        for key, value in user_answers.items():
            cleaned_user_answers[key] = self._clean_input(value)

        # updated state
        self._user_journey_manager.update_state(location, user_answers)

        # get the current location in the questionnaire
        current_location = self._user_journey_manager.get_current_location()

        # run the validator to update the validation_store
        if self._user_journey_manager.validate():

            # process the user action
            self._user_action_processor.process_action(user_action)

            # do any routing
            next_location = self._routing_engine.get_next_location(current_location)
            logger.info("next location after routing is %s", next_location)

            # go to that location
            self._user_journey_manager.go_to_state(next_location)
            logger.debug("Going to location %s", next_location)
        else:
            # bug fix for using back button which then fails validation
            self._user_journey_manager.go_to_state(current_location)

        self._pre_processor.initialize()
        # now return the location
        return self._user_journey_manager.get_current_location()

    def get_rendering_context(self):
        return self._pre_processor.build_view_data()

    def get_rendering_template(self):
        return self._pre_processor.get_template_name()

    def _process_incoming_post_data(self, post_data):
        user_answers = {}
        user_action = None

        for key in post_data.keys():
            if key.startswith('action['):
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
        return self._user_journey_manager.get_current_location()

    def delete_user_data(self):
        # once the survey has been submitted
        # delete all user data from the database
        current_user.delete_questionnaire_data()
        # and clear out the session state
        session_manager.clear()

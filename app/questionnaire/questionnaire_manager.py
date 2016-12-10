import logging

from app.globals import get_answer_store, get_answers, get_metadata, get_questionnaire_store
from app.questionnaire.navigator import Navigator
from app.questionnaire.rules import evaluate_rule, get_metadata_value

from app.templating.schema_context import build_schema_context
from app.templating.template_renderer import renderer

from flask import g

from flask_login import current_user

logger = logging.getLogger(__name__)


def get_questionnaire_manager(schema, schema_json):
    questionnaire_manager = g.get('_questionnaire_manager')
    if questionnaire_manager is None:
        questionnaire_manager = g._questionnaire_manager = QuestionnaireManager(schema, schema_json)

    return questionnaire_manager


class QuestionnaireManager(object):

    """
    This class represents a user journey through a survey. It models the request/response process of the web application
    """
    def __init__(self, schema, json=None):
        self._json = json
        self._schema = schema
        self.state = None

    def validate(self, location, post_data):

        self.build_state(location, post_data)

        if self.state:
            # Todo, this doesn't feel right, validation is casting the user values to their type.
            return self.state.schema_item.validate(self.state)
        else:
            # Item has node, but is not in schema: must be introduction, thank you or summary
            return True

    def validate_all_answers(self):
        navigator = Navigator(self._json, get_metadata(current_user), get_answer_store(current_user))

        for location in navigator.get_location_path():
            answers = get_answers(current_user)
            is_valid = self.validate(location, answers)

            if not is_valid:
                logger.debug("Failed validation with current location %s", str(location))
                return False, location

        return True, None

    def update_questionnaire_store(self, location):
        # Store answers in QuestionnaireStore
        questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)

        for answer in self.get_state_answers(location['block_id']):
            questionnaire_store.answer_store.add_or_update(answer.flatten())

        if location not in questionnaire_store.completed_blocks:
            questionnaire_store.completed_blocks.append(location)

        questionnaire_store.save()

    def process_incoming_answers(self, location, post_data):
        logger.debug("Processing post data for %s", location)

        is_valid = self.validate(location, post_data)
        # run the validator to update the validation_store
        if is_valid:
            self.update_questionnaire_store(location)

        return is_valid

    def build_state(self, location, answers):
        # Build the state from the answers
        self.state = None
        if self._schema.item_exists(location['block_id']):
            metadata = get_metadata(current_user)
            answer_store = get_answer_store(current_user)
            schema_item = self._schema.get_item_by_id(location['block_id'])

            self.state = schema_item.construct_state()
            for answer in self.get_state_answers(location['block_id']):
                answer.group_id = location['group_id']
                answer.group_instance = location['group_instance']
            self.state.update_state(answers)
            self._conditional_display(self.state)

            context = build_schema_context(metadata, self._schema.aliases, answer_store, location['group_instance'])
            renderer.render_state(self.state, context)

    def get_state_answers(self, item_id):
        # get the answers from the state
        if self._schema.item_exists(item_id):
            return self.state.get_answers()

        return []

    def _conditional_display(self, item):
        # Process any conditional display rules

        if item.schema_item:

            item.skipped = False

            if hasattr(item.schema_item, 'skip_condition') and item.schema_item.skip_condition:
                rule = item.schema_item.skip_condition.as_dict()
                when = rule['when']

                if 'id' in when and when['id']:
                    answer = get_answers(current_user).get(when['id'])
                    item.skipped = evaluate_rule(when, answer)

                if 'meta' in when and when['meta']:
                    value = get_metadata_value(get_metadata(current_user), when['meta'])
                    item.skipped = evaluate_rule(when, value)

            for child in item.children:
                self._conditional_display(child)

    def get_schema_item_by_id(self, item_id):
        return self._schema.get_item_by_id(item_id)

    def get_schema(self):
        return self._schema

    def add_answer(self, location, question_id, answer_store):
        question_schema = self._schema.get_item_by_id(question_id)
        question_state = self.state.find_state_item(question_schema)

        for answer_schema in question_schema.answers:
            next_answer_instance_id = self._get_next_answer_instance(answer_store, answer_schema.id)
            new_answer_state = question_state.create_new_answer_state(answer_schema, next_answer_instance_id)
            question_state.add_new_answer_state(new_answer_state)

        self.update_questionnaire_store(location)

    @staticmethod
    def _get_next_answer_instance(answer_store, answer_id):
        existing_answers = answer_store.filter(answer_id=answer_id)
        last_answer = existing_answers[-1:]
        next_answer_instance_id = 0 if len(last_answer) == 0 else int(last_answer[0]['answer_instance']) + 1
        return next_answer_instance_id

    def remove_answer(self, location, answer_store, index_to_remove):
        state_answers = self.state.get_answers()
        for state_answer in state_answers:
            if state_answer.answer_instance == index_to_remove:
                question = state_answer.parent
                question.remove_answer(state_answer)
                answer_store.remove_answer(state_answer.flatten())

        self.update_questionnaire_store(location)

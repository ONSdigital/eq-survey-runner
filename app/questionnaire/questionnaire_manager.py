import copy
import logging

from app.globals import get_answer_store, get_answers, get_metadata, get_questionnaire_store
from app.questionnaire.navigator import Navigator, evaluate_rule
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

    '''
    This class represents a user journey through a survey. It models the request/response process of the web application
    '''
    def __init__(self, schema, json=None):
        self._json = json
        self._schema = schema
        self.state = None

        self.navigator = Navigator(self._json)

    def validate(self, location, post_data):

        answers = get_answers(current_user)

        if location in self.navigator.get_location_path(answers):

            self.build_state(location, post_data)

            if self.state:
                # Todo, this doesn't feel right, validation is casting the user values to their type.
                return self.state.schema_item.validate(self.state)
            else:
                # Item has node, but is not in schema: must be introduction, thank you or summary
                return True
        else:
            # Not a validation location, so can't be valid
            return False

    def validate_all_answers(self):

        answers = get_answers(current_user)

        for location in self.navigator.get_location_path(answers):
            is_valid = self.validate(location, answers)

            if not is_valid:
                logger.debug("Failed validation with current location %s", location)
                return False, location

        return True, None

    def process_incoming_answers(self, location, post_data):
        logger.debug("Processing post data for %s", location)

        is_valid = self.validate(location, post_data)
        # run the validator to update the validation_store
        if is_valid:
            self.update_questionnaire_store(location)

        return is_valid

    def update_questionnaire_store(self, location):
        # Store answers in QuestionnaireStore
        questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)
        for answer in self.get_state_answers(location):
            questionnaire_store.answers.add(answer.flatten())

        if location not in questionnaire_store.completed_blocks:
            questionnaire_store.completed_blocks.append(location)

        questionnaire_store.save()

    def build_state(self, item_id, answers):
        # Build the state from the answers
        self.state = None
        if self._schema.item_exists(item_id):
            schema_item = self._schema.get_item_by_id(item_id)
            self.state = schema_item.construct_state(answers)
            self.state.update_state(answers)
            self._conditional_display(self.state)
        if self.state:
            context = build_schema_context(get_metadata(current_user), self._schema.aliases, answers)
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
                answer = get_answers(current_user).get(rule['when']['id'])

                item.skipped = evaluate_rule(rule, answer)

            for child in item.children:
                self._conditional_display(child)

    def get_schema_item_by_id(self, item_id):
        return self._schema.get_item_by_id(item_id)

    def get_schema(self):
        return self._schema

    def add_answer(self, block, question, post_data):
        if self.state is None:
            self.process_incoming_answers(block, post_data)

        question_schema = self._schema.get_item_by_id(question)
        question_state = self.state.find_state_item(question_schema)

        answer_schema = question_schema.answers[0]  # Single answer for now.
        new_answer = self._create_new_answer(answer_schema, question_state)

        question_answers = question_state.children
        question_answers.append(new_answer)

        self.update_questionnaire_store(block)

    @classmethod
    def _create_new_answer(cls, answer_schema, question_state):
        new_answer = answer_schema.construct_state()

        answer_store = get_answer_store(current_user)
        existing = answer_store.filter({
          'answer_id': answer_schema.id,
        })
        last_answer = existing[-1:]
        next_instance_id = 0 if len(last_answer) == 0 else int(last_answer[0]['answer_instance']) + 1
        new_answer_schema = copy.deepcopy(new_answer.schema_item)
        new_answer_schema.widget.name += '_' + str(next_instance_id)
        new_answer.schema_item = new_answer_schema
        new_answer.parent = question_state
        new_answer.instance = next_instance_id
        return new_answer

    def remove_answer(self, block, question, post_data):
        if self.state is None:
            self.process_incoming_answers(block, post_data)

        index_to_remove = post_data.get('action[remove_answer]')
        answer = self.state.get_answers()[int(index_to_remove)]
        question = answer.parent
        question.remove_answer(answer)

        answer_store = get_answer_store(current_user)
        answer_store.remove(answer.flatten())
        self.update_questionnaire_store(block)

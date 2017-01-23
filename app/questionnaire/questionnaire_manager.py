import logging

from flask import g
from flask_login import current_user

from app.globals import get_answer_store, get_answers, get_metadata, get_questionnaire_store
from app.questionnaire.path_finder import PathFinder
from app.schema.block import Block
from app.schema.exceptions import QuestionnaireException

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
        self.block_state = None

    def validate(self, location, post_data, skip_mandatory_validation=False):

        self.build_block_state(location, post_data)
        return location.is_interstitial() or self.block_state.schema_item.validate(self.block_state, skip_mandatory_validation)

    def validate_all_answers(self):

        navigator = PathFinder(self._json, get_answer_store(current_user), get_metadata(current_user))

        for location in navigator.get_location_path():
            answers = get_answers(current_user)
            is_valid = self.validate(location, answers)

            if not is_valid:
                logger.debug("Failed validation with current location %s", str(location))
                return False, location

        return True, None

    def update_questionnaire_store(self, location):
        questionnaire_store = self._add_update_answer_store(location)

        if location not in questionnaire_store.completed_blocks:
            questionnaire_store.completed_blocks.append(location)

    def update_questionnaire_store_save_sign_out(self, location):
        questionnaire_store = self._add_update_answer_store(location)

        if location in questionnaire_store.completed_blocks:
            questionnaire_store.completed_blocks.remove(location)

    def _add_update_answer_store(self, location):
        questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)
        for answer in self.get_state_answers(location.block_id):
            questionnaire_store.answer_store.add_or_update(answer.flatten())
        return questionnaire_store

    def process_incoming_answers(self, location, post_data):
        logger.debug("Processing post data for %s", location)

        is_valid = self.validate(location, post_data)
        # run the validator to update the validation_store
        if is_valid:
            self.update_questionnaire_store(location)

        return is_valid

    def build_block_state(self, location, answers):
        # Build the state from the answers
        self.block_state = None
        if self._schema.item_exists(location.block_id):
            metadata = get_metadata(current_user)
            block = self._schema.get_item_by_id(location.block_id)
            if not isinstance(block, Block):
                raise QuestionnaireException
            self.block_state = block.construct_state()

            for answer in self.get_state_answers(location.block_id):
                answer.group_id = location.group_id
                answer.group_instance = location.group_instance
            self.block_state.update_state(answers)
            self.block_state.set_skipped(get_answers(current_user), metadata)

    def get_state_answers(self, item_id):
        # get the answers from the state
        if self._schema.item_exists(item_id):
            return self.block_state.get_answers()

        return []

    def get_schema_item_by_id(self, item_id):
        return self._schema.get_item_by_id(item_id)

    def get_schema(self):
        return self._schema

    def add_answer(self, location, answer_store, question_id):
        question_schema = self._schema.get_item_by_id(question_id)
        question_state = self.block_state.find_state_item(question_schema)

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
        state_answers = self.block_state.get_answers()
        for state_answer in state_answers:
            if state_answer.answer_instance == index_to_remove:
                question = state_answer.parent
                question.remove_answer(state_answer)
                answer_store.remove_answer(state_answer.flatten())

        self.update_questionnaire_store(location)

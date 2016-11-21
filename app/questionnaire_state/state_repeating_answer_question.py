import copy
import re

from app.data_model.answer_store import natural_order
from app.questionnaire_state.state_answer import StateAnswer
from app.questionnaire_state.state_question import StateQuestion


class RepeatingAnswerStateQuestion(StateQuestion):
    def __init__(self, question_id, schema_item):
        super().__init__(id=question_id, schema_item=schema_item)

    def update_state(self, user_input):
        self.build_repeating_state(user_input)
        for state_answer in self.answers:
            state_answer.update_state(user_input)

    def build_repeating_state(self, user_input):
        for answer_id, answer_index in self.iterate_over_instance_ids(user_input.keys()):
            for answer_schema in self.schema_item.answers:
                if answer_schema.id == answer_id:
                    self.create_new_answer_state(answer_schema, answer_index)
                    break

    def create_new_answer_state(self, answer_schema, answer_instance):
        for answer_state in self.answers:
            if answer_schema.id == answer_state.id and answer_instance == answer_state.answer_instance:
                return None

        new_answer_schema = copy.deepcopy(answer_schema)
        suffix = '_' + str(answer_instance) if answer_instance > 0 else ''
        widget_id = answer_schema.id + suffix
        new_answer_schema.widget = type(answer_schema.widget)(widget_id)
        new_answer_state = StateAnswer(new_answer_schema.id, new_answer_schema)
        new_answer_state.answer_instance = answer_instance
        new_answer_state.parent = self
        self.answers.append(new_answer_state)

    @classmethod
    def iterate_over_instance_ids(cls, answer_instances):
        """
        Iterates over a collection of answer instances yielding the answer Id and answer instance Id.
        :param answer_instances: A list of raw answer_instance_ids
        :return: Tuple containing the answer Id and answer instance Id.
        """

        answer_instance_ids = sorted(answer_instances, key=natural_order)

        for answer_instance_id in answer_instance_ids:
            answer_id, answer_index = cls._extract_answer_instance_id(answer_instance_id)
            yield answer_id, answer_index

    @staticmethod
    def _extract_answer_instance_id(answer_instance_id):
        matches = re.match(r'^(.+?)_(\d+)$', answer_instance_id)
        if matches:
            answer_id, index = matches.groups()
        else:
            answer_id = answer_instance_id
            index = 0

        return answer_id, int(index)

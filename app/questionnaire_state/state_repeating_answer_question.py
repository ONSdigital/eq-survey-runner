import copy
import re

from collections import defaultdict
from collections import OrderedDict

from app.data_model.answer_store import natural_order
from app.questionnaire_state.state_answer import StateAnswer
from app.questionnaire_state.state_question import StateQuestion


class RepeatingAnswerStateQuestion(StateQuestion):
    def __init__(self, id, schema_item):
        super().__init__(id=id, schema_item=schema_item)

    def update_state(self, user_input):
        self.build_repeating_state(user_input)
        self.children = self.answers
        for state_answer in self.answers:
            state_answer.update_state(user_input)

    def build_repeating_state(self, user_input):
        for answer_id, answer_index in iterate_over_instance_ids(user_input.keys()):
            for answer_schema in self.schema_item.answers:
                if answer_schema.id == answer_id and self.is_new_answer_state_required(answer_schema, answer_index):
                    new_answer_state = self.create_new_answer_state(answer_schema, answer_index)
                    self.add_new_answer_state(new_answer_state)
                    break

    def is_new_answer_state_required(self, answer_schema, answer_instance):
        for answer_state in self.answers:
            if answer_schema.id == answer_state.id and answer_instance == answer_state.answer_instance:
                return False
        return True

    def create_new_answer_state(self, answer_schema, answer_instance, group_instance=0):
        new_answer_schema = copy.copy(answer_schema)
        suffix = '_' + str(answer_instance) if answer_instance > 0 else ''
        widget_id = answer_schema.id + suffix
        new_answer_schema.widget = type(answer_schema.widget)(widget_id)
        new_answer_state = StateAnswer(new_answer_schema.id, new_answer_schema)
        new_answer_state.answer_instance = answer_instance
        new_answer_state.group_instance = group_instance
        new_answer_state.parent = self
        return new_answer_state

    def add_new_answer_state(self, answer_state):
        self.answers.append(answer_state)

    def answers_grouped_by_instance(self):
        """
        Groups answers by their answer_instance Id.
        :return: A list of lists containing the answers grouped by answer_instance.
        """

        answer_states_by_id = defaultdict(list)
        for answer_state in self.answers:
            answer_states_by_id[answer_state.id].append(answer_state)

        answer_states_grouped_by_instance = OrderedDict()
        for answer_schema in self.schema_item.answers:
            answer_states = answer_states_by_id.get(answer_schema.id)
            if answer_states:
                for answer_state in answer_states:
                    answer_states_grouped_by_instance.setdefault(answer_state.answer_instance, []).append(answer_state)

        return list(answer_states_grouped_by_instance.values())


def iterate_over_instance_ids(answer_instances):
    """
    Iterates over a collection of answer instances yielding the answer Id and answer instance Id.
    :param answer_instances: A list of raw answer_instance_ids
    :return: Tuple containing the answer Id and answer instance Id.
    """

    answer_instance_ids = sorted(answer_instances, key=natural_order)

    for answer_instance_id in answer_instance_ids:
        answer_id, answer_index = extract_answer_instance_id(answer_instance_id)
        yield answer_id, answer_index


def extract_answer_instance_id(answer_instance_id):
    matches = re.match(r'^(.+?)_(\d+)$', answer_instance_id)
    if matches:
        answer_id, index = matches.groups()
    else:
        answer_id = answer_instance_id
        index = 0

    return answer_id, int(index)

import re

from app.data_model.answer_store import natural_order
from app.questionnaire_state.state_item import StateItem


class StateQuestion(StateItem):
    def __init__(self, id, schema_item):
        super(StateQuestion, self).__init__(id=id, schema_item=schema_item)
        self.answers = []
        self.children = self.answers

    def remove_answer(self, answer):
        if answer in self.answers:
            self.answers.remove(answer)

    def update_state(self, user_input):
        if self.schema_item.type == 'RepeatingAnswer':
            self.build_repeating_state(user_input)
            for state_answer in self.answers:
                state_answer.update_state(user_input)
        else:
            super(StateQuestion, self).update_state(user_input)

    def build_repeating_state(self, user_input):
        for answer_id, answer_index in self._iterate_over_instance_ids(user_input):
            for answer_schema in self.schema_item.answers:
                if answer_schema.id == answer_id:
                    new_state = answer_schema.create_new_answer_state(self.answers, answer_index)
                    if new_state:
                        new_state.parent = self
                        self.answers.append(new_state)
                    break

    @classmethod
    def _iterate_over_instance_ids(cls, user_input):

        answer_instance_ids = [key for key in user_input]
        answer_instance_ids = sorted(answer_instance_ids, key=natural_order)

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

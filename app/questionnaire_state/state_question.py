from app.questionnaire_state.state_item import StateItem


class StateQuestion(StateItem):
    def __init__(self, id, schema_item):
        super().__init__(id=id, schema_item=schema_item)
        self.answers = []
        self.children = self.answers

    def remove_answer(self, answer):
        if answer in self.answers:
            self.answers.remove(answer)

    def update_state(self, user_input):
        if self.schema_item.type == 'RepeatingAnswer':
            self.build_repeating_answers(user_input)
        else:
            super(StateQuestion, self).update_state(user_input)

    def build_repeating_answers(self, user_input):
        state_answers = self.children[:]
        for child in state_answers:
            answer_keys = [key if key.startswith(child.schema_item.id) else None for key in user_input]
            answer_instances = sorted(list(filter(None, answer_keys)))
            num_instances = len(answer_instances)

            for index in range(num_instances):
                if index == 0:
                    child.update_state(user_input)
                else:
                    new_answer_state = self._create_new_answer_state(child.schema_item, index, answer_instances)
                    new_answer_state.update_state(user_input)

    def _create_new_answer_state(self, answer_schema, index, instances):
        next_answer_instance_id = self._next_answer_instance_id(instances, answer_schema.id, index)
        new_answer = answer_schema.create_new_answer_state(answer_instance=next_answer_instance_id, parent=self)
        return new_answer

    @staticmethod
    def _next_answer_instance_id(answer_instances, answer_id, index):
        num_instances = len(answer_instances)
        if num_instances == 0:
            return index
        else:
            current_instance = answer_instances[index]
            instance_suffix = current_instance.replace(answer_id, '').replace('_', '')
            next_answer_instance_id = 0 if instance_suffix == '' else int(instance_suffix)
            return next_answer_instance_id

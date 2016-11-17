import copy

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
            state_answers = self.children[:]

            for child in state_answers:
                answer_keys = [key if key.startswith(child.schema_item.id) else None for key in user_input]
                answer_instances = sorted(list(filter(None, answer_keys)))
                num_instances = len(answer_instances)

                if num_instances > 1:
                    for index in range(num_instances):
                        if index == 0:
                            child.update_state(user_input)
                        else:
                            new_answer = self._add_new_answer(child.schema_item, index, answer_instances)
                            new_answer.update_state(user_input)
                else:
                    child.update_state(user_input)
        else:
            super(StateQuestion, self).update_state(user_input)

    def _add_new_answer(self, answer_schema, index, instances):
        new_answer = answer_schema.construct_state()
        new_answer.parent = self

        instance_id = self._get_instance_id(instances, answer_schema.id, index)
        new_answer.answer_instance = instance_id

        new_answer_schema = copy.deepcopy(answer_schema)
        new_answer_schema.widget.name += '_' + str(instance_id) if instance_id > 0 else ''
        new_answer.schema_item = new_answer_schema

        self.children.append(new_answer)
        return new_answer

    @staticmethod
    def _get_instance_id(answer_instances, answer_id, index):
        num_instances = len(answer_instances)
        if num_instances == 0:
            instance_id = index
        else:
            current_instance = answer_instances[index]
            instance_suffix = current_instance.replace(answer_id, '').replace('_', '')
            instance_id = 0 if instance_suffix == '' else int(instance_suffix)
        return instance_id

import copy

from app.schema.question import Question


class RepeatingAnswerQuestion(Question):
    """
    A Question type that supports repeating answers.
    """
    def __init__(self):
        super().__init__()
        self.max_repeats = None

    def construct_state(self, answers=None):
        schema_answers = [schema_answer for schema_answer in self.answers]

        state_class = self.get_state_class()
        question_state = state_class(self.id, self)

        for answer_schema in schema_answers:
            answer_instances = \
              sorted(list(
                filter(None, [answer_id if answer_id.startswith(answer_schema.id) else None for answer_id in answers])))

            count_instances = len(answer_instances)
            repeat = 1 if count_instances == 0 else count_instances

            for i in range(repeat):
                answer_state = answer_schema.construct_state(schema_answers)
                answer_state.parent = question_state

                instance_id = self._get_answer_instance(answer_instances, answer_schema.id, i, count_instances)
                answer_state.instance = instance_id

                new_answer_schema = copy.deepcopy(answer_schema)
                if instance_id > 0:
                    new_answer_schema.widget.name += '_' + str(instance_id)

                answer_state.schema_item = new_answer_schema
                question_state.children.append(answer_state)

        return question_state

    @classmethod
    def _get_answer_instance(cls, answer_instances, answer_id, i, num_instances):
        if num_instances == 0:
            instance_id = i
        else:
            current_instance = answer_instances[i]
            instance_suffix = current_instance.replace(answer_id, '').replace('_', '')
            instance_id = 0 if instance_suffix == '' else int(instance_suffix)
        return instance_id

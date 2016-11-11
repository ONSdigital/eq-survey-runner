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
                sorted(
                    list(
                        filter(None, [id if id.startswith(answer_schema.id) else None for id in answers])
                    )
                )

            num_instances = len(answer_instances)
            repeat = 1 if num_instances == 0 else num_instances

            for i in range(repeat):
                answer_state = answer_schema.construct_state(schema_answers)
                answer_state.parent = question_state

                if num_instances == 0:
                    instance_id = i
                else:
                    current_instance = answer_instances[i]
                    instance_suffix = current_instance.replace(answer_schema.id, '')
                    instance_id = 0 if instance_suffix == '' else int(instance_suffix)

                answer_state.instance = instance_id

                new_answer_schema = copy.deepcopy(answer_schema)
                new_answer_schema.widget.name += str(instance_id) if instance_id > 0 else ''
                answer_state.schema_item = new_answer_schema

                question_state.children.append(answer_state)

        return question_state

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
        return self._construct_state_from_dict(answers)

    def _construct_state_from_dict(self, post_vars=None):
        schema_answers = [schema_answer for schema_answer in self.answers]

        state_class = self.get_state_class()
        state = state_class(self.id, self)

        for schema_answer in schema_answers:
            instances = list(filter(None, [name if name.startswith(schema_answer.id) else None for name in post_vars]))

            number_of_instances = len(instances)
            repeat = 1 if number_of_instances == 0 else number_of_instances

            for i in range(repeat):
                answer_state = schema_answer.construct_state(schema_answers)
                answer_state.parent = state
                answer_state.instance = i

                new_answer_schema = copy.deepcopy(schema_answer)
                new_answer_schema.widget.name += str(i) if i > 0 else ''

                answer_state.schema_item = new_answer_schema

                state.children.append(answer_state)

        return state

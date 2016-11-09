from app.schema.question import Question


class RepeatingAnswerQuestion(Question):
    """
    A Question type that supports repeating answers.
    """
    def __init__(self):
        super().__init__()
        self.max_repeats = None

    def construct_state(self, answers=None):
        if answers is None:
            return super(RepeatingAnswerQuestion, self).construct_state(answers)

        elif isinstance(answers, dict):
            return self._construct_state_from_dict(answers)

        else:
            return self._construct_from_answer_store(answers)

    def _construct_state_from_dict(self, post_vars=None):
        schema_answers = [schema_answer for schema_answer in self.answers]

        state_class = self.get_state_class()
        state = state_class(self.id, self)

        for schema_answer in schema_answers:
            instances = list(filter(None, [name if name.startswith(schema_answer.id) else None for name in post_vars]))
            for answer in instances:
                widget_answer = {
                  schema_answer.id: post_vars.get(answer)
                }
                index = answer.replace(schema_answer.id, '')
                instance = 0 if index == '' else int(index)
                answer_state = schema_answer.construct_state(widget_answer)
                answer_state.parent = state
                answer_state.instance = instance
                state.children.append(answer_state)

        return state

    def _construct_from_answer_store(self, answers=None):
        answer_count = len(answers.find_by_question(self.id))

        state_class = self.get_state_class()
        if state_class:
            state = state_class(self.id, self)

            repeat = 1 if answer_count == 0 else answer_count
            for i in range(repeat):
                for child in self.children:
                    child_state = child.construct_state(answers)
                    child_state.parent = state
                    state.children.append(child_state)
                    return state
        else:
            return None

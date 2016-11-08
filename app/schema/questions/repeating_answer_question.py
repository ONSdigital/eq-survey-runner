from app.schema.question import Question


class RepeatingAnswerQuestion(Question):
    """
    A Question type that supports repeating answers.
    """
    def __init__(self):
        super().__init__()
        self.max_repeats = None

    def construct_state(self, answers=None):
        if answers is None or isinstance(answers, dict):
            return super(RepeatingAnswerQuestion, self).construct_state(answers)

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

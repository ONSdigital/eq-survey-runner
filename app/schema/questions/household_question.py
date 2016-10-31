from app.schema.question import Question


class HouseholdQuestion(Question):
    def __init__(self):
        super().__init__()

    def add_new_answer(self, answer):
        super(HouseholdQuestion, self).add_answer(answer)
        self.children.append(answer)

    def construct_state(self, answers=None):
        if answers is None:
            return super(HouseholdQuestion, self).construct_state(answers)

        num_answers = HouseholdQuestion._get_num_answers(answers)

        state_class = self.get_state_class()
        if state_class:
            state = state_class(self.id, self)

            repeat = 1 if num_answers == 0 else num_answers
            for i in range(repeat):
                for child in self.children:
                    child_state = child.construct_state(answers)
                    child_state.parent = state
                    state.children.append(child_state)
            return state
        else:
            return None

    @staticmethod
    def _get_num_answers(answers):
        all_keys = [key.split('-')[0] if key.startswith('person') else '' for key in answers]
        unique_answers = set(filter(None, all_keys))
        return len(unique_answers)

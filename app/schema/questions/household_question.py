from app.schema.question import Question


class HouseholdQuestion(Question):
    def __init__(self):
        super().__init__()

    def add_new_answer(self, answer):
        super(HouseholdQuestion, self).add_answer(answer)
        self.children.append(answer)

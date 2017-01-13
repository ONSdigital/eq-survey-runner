from app.questionnaire_state.state_item import StateItem


class StateQuestion(StateItem):
    def __init__(self, item_id, schema_item):
        super().__init__(item_id=item_id, schema_item=schema_item)
        self.answers = []
        self.children = self.answers

    def remove_answer(self, answer):
        if answer in self.answers:
            self.answers.remove(answer)

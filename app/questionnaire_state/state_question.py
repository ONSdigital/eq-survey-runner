from app.questionnaire_state.state_item import StateItem
from app.data_model.answer_store import AnswerStore


class StateQuestion(StateItem):
    def __init__(self, id, schema_item):
        super().__init__(id=id, schema_item=schema_item)
        self.answers = []
        self.children = self.answers

    def remove_answer(self, answer):
        if answer in self.answers:
            self.answers.remove(answer)

        if answer in self.children:
            self.children.remove(answer)

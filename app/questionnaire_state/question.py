from app.questionnaire_state.answer import Answer
from app.questionnaire_state.item import Item


class Question(Item):
    def __init__(self, id):
        super().__init__(id=id)
        self.answers = []
        self.children = self.answers

    @staticmethod
    def construct_state(item):
        state = Question(item.id)
        for child in item.children:
            child_state = Answer.construct_state(child)
            state.children.append(child_state)
        return state

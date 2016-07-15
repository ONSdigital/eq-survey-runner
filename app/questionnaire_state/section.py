from app.questionnaire_state.question import Question
from app.questionnaire_state.item import Item


class Section(Item):
    def __init__(self, id):
        super().__init__(id=id)
        self.questions = []
        self.children = self.questions

    @staticmethod
    def construct_state(item):
        state = Section(item.id)
        for child in item.children:
            child_state = Question.construct_state(child)
            state.children.append(child_state)
        return state

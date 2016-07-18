from app.questionnaire_state.item import Item
from app.questionnaire_state.section import Section


class Block(Item):

    def __init__(self, id):
        super().__init__(id=id)
        self.sections = []
        self.children = self.sections

    @staticmethod
    def construct_state(item):
        state = Block(item.id)
        for child in item.children:
            child_state = Section.construct_state(child)
            state.children.append(child_state)
        return state

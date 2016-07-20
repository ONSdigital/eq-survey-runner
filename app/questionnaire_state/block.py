from app.questionnaire_state.item import Item


class Block(Item):

    def __init__(self, id):
        super().__init__(id=id)
        self.sections = []
        self.children = self.sections

from app.questionnaire_state.item import Item


class Section(Item):
    def __init__(self, id):
        super().__init__(id=id)
        self.questions = []
        self.children = self.questions

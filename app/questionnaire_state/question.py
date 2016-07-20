from app.questionnaire_state.item import Item


class Question(Item):
    def __init__(self, id):
        super().__init__(id=id)
        self.answers = []
        self.children = self.answers

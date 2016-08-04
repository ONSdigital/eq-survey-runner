from app.questionnaire_state.item import Item


class Section(Item):
    def __init__(self, id, schema_item):
        super().__init__(id=id, schema_item=schema_item)
        self.questions = []
        self.children = self.questions

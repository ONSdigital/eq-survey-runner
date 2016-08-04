from app.questionnaire_state.item import Item


class Block(Item):

    def __init__(self, id, schema_item):
        super().__init__(id=id, schema_item=schema_item)
        self.sections = []
        self.children = self.sections

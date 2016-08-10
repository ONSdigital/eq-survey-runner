from app.questionnaire_state.item import Item


class Confirmation(Item):

    def __init__(self, id):
        super().__init__(id=id, schema_item=None)

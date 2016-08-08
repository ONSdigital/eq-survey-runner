from app.questionnaire_state.item import Item


class ThankYou(Item):

    def __init__(self, id, submitted_at):
        super().__init__(id=id, schema_item=None)
        self.submitted_at = submitted_at
        self.display_on_summary = False

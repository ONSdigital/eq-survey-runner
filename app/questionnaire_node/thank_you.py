from app.questionnaire_node.state_item import StateItem


class ThankYou(StateItem):

    def __init__(self, id, submitted_at):
        super().__init__(id=id, schema_item=None)
        self.submitted_at = submitted_at
        self.display_on_summary = False

from app.questionnaire_node.state_item import StateItem


class Summary(StateItem):

    def __init__(self, id):
        super().__init__(id=id, schema_item=None)
        self.display_on_summary = False

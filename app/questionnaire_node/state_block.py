from app.questionnaire_node.state_item import StateItem


class StateBlock(StateItem):

    def __init__(self, id, schema_item):
        super().__init__(id=id, schema_item=schema_item)
        self.sections = []
        self.children = self.sections

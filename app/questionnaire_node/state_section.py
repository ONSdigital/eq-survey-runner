from app.questionnaire_node.state_item import StateItem


class StateSection(StateItem):
    def __init__(self, id, schema_item):
        super().__init__(id=id, schema_item=schema_item)
        self.questions = []
        self.children = self.questions

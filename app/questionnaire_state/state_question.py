from app.questionnaire_state.state_item import StateItem


class StateQuestion(StateItem):
    def __init__(self, id, schema_item):
        super().__init__(id=id, schema_item=schema_item)
        self.answers = []
        self.children = self.answers

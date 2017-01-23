from app.questionnaire_state.state_item import StateItem


class StateBlock(StateItem):

    def __init__(self, item_id, schema_item):
        super().__init__(item_id=item_id, schema_item=schema_item)
        self.sections = []
        self.children = self.sections

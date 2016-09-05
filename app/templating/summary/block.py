from app.templating.summary.summary_item import SummaryItem


class Block(object):
    def __init__(self, schema, state):
        self.schema = schema
        self.state = state
        self.items = self.build_summary_items(self.state, self.schema)
        self.title = self.schema.title

    def build_summary_items(self, state, schema):
        items = []

        for question_state in state.questions:
            if question_state.display_on_summary:
                items.append(SummaryItem.create_item(schema.questionnaire.get_item_by_id(question_state.id), question_state))

        return items

from app.templating.summary.item import Item as SummaryItem

from flask import render_template


class Block(object):
    template_name = 'partials/summary/block.html'

    def __init__(self, schema, state):
        self.schema = schema
        self.state = state

    def render(self):
        template_params = {
            'title': self.schema.title,
            'items': self.build_summary_items(self.state, self.schema),
            'id': self.state.id,
        }
        return render_template(Block.template_name, **template_params)

    def build_summary_items(self, state, schema):
        items = []

        for section_state in state.sections:
            for question_state in section_state.questions:
                if question_state.display_on_summary:
                    items.append(SummaryItem.create_item(schema.questionnaire.get_item_by_id(question_state.id), question_state))

        return items

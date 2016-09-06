from app.templating.summary.items.date_range_summary import DateRangeSummaryItem
from app.templating.summary.items.general_summary import GeneralSummaryItem

from app.utilities.factory import Factory


class Block(object):
    def __init__(self, schema, state):
        self.schema = schema
        self.state = state
        self.items = self.build_summary_items(self.state, self.schema)

    def build_summary_items(self, state, schema):
        items = []

        question_factory = Factory()
        question_factory.register_all({
            "DATERANGE": DateRangeSummaryItem,
            "GENERAL": GeneralSummaryItem,
        })

        for question_state in state.questions:
            if question_state.display_on_summary:
                schema_item = schema.questionnaire.get_item_by_id(question_state.id)

                item = question_factory.create(schema_item.type.upper(), schema_item, question_state)

                items.append(item)

        return items

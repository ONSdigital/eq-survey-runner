import logging

from app.templating.summary.summary_item import SummaryItem

logger = logging.getLogger(__name__)


class SummarySection(object):
    def __init__(self, schema, state):
        self.schema = schema
        self.state = state
        self.items = self.build_section_items(self.state, self.schema)
        self.title = self.schema.title
        self.id = self.schema.id

    # Prepare each section for the frontend
    @staticmethod
    def build_section_items(state, schema):

        summary_items = []
        for question_state in state.questions:

            # Check if conditional display has been triggered on a question
            if not question_state.skipped:
                logger.debug("Preparing summary item %s", question_state.id)
                schema_item = schema.questionnaire.get_item_by_id(question_state.id)
                summary_item = SummaryItem(schema_item, question_state.answers, schema_item.type.upper())
                summary_items.append(summary_item)

        return summary_items

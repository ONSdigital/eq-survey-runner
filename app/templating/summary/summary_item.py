import logging

from app.templating.summary.summary_sub_item import SummarySubItem

logger = logging.getLogger(__name__)


class SummaryItem(object):
    def __init__(self, schema, state_answers, question_type):
        self.question = schema.title or schema.answers[0].label
        self.type = schema.answers[0].type.lower()
        self.sub_items = SummaryItem.build_sub_items(schema, state_answers, question_type)

    @staticmethod
    def build_sub_items(schema, state_answers, question_type):
        sub_items = []
        state_answers_iterator = iter(state_answers)
        for answer in state_answers_iterator:
            sub_items.append(SummarySubItem(schema, state_answers, question_type, answer))
            if question_type == 'DATERANGE':
                next(state_answers_iterator)
        return sub_items

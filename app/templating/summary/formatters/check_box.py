import logging

from app.templating.summary.formatters.abstract_formater import AbstractFormatter

logger = logging.getLogger(__name__)


class CheckBoxFormatter(AbstractFormatter):

    @staticmethod
    def format(schema_answers, state_answers, user_answer):
        answers = []

        for option in schema_answers[0].options:
            if option['value'] in user_answer:
                answers.append(option['label'])

        return answers

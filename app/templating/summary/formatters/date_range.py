from datetime import datetime

from app.templating.summary.formatters.abstract_formatter import AbstractFormatter


class DateRangeFormatter(AbstractFormatter):

    @staticmethod
    def format(schema_answers, state_answers, user_answer):
        answer = [{
            'label': schema_answers[0].label,
            'value': datetime.strptime(state_answers[0].value, "%d/%m/%Y"),
        }, {
            'label': schema_answers[1].label,
            'value': datetime.strptime(state_answers[1].value, "%d/%m/%Y"),
        }]
        return answer

from app.templating.summary.formatters.abstract_formater import AbstractFormatter


class DateRangeFormatter(AbstractFormatter):

    @staticmethod
    def format(schema_answers, state_answers, user_answer):
        answer = [{
            'label': schema_answers[0].label,
            'value': state_answers[0].value,
        }, {
            'label': schema_answers[1].label,
            'value': state_answers[1].value,
        }]
        return answer

from app.templating.summary.formatters.abstract_formatter import AbstractFormatter


class RadioButtonFormatter(AbstractFormatter):

    @staticmethod
    def format(schema_answers, state_answers, user_answer):
        for option in schema_answers[0].options:
            if option['value'] == user_answer:
                if option['label'] == 'Other':
                    return state_answers[0].other if state_answers and state_answers[0].other else user_answer
                else:
                    return option['label']

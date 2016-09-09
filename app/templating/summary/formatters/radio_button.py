from app.templating.summary.formatters.abstract_formater import AbstractFormatter


class RadioButtonFormatter(AbstractFormatter):

    @staticmethod
    def format(schema_answers, state_answers, user_answer):
        for option in schema_answers[0].options:
            if option['value'] == user_answer:
                return option['label']

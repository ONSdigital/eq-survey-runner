from app.templating.summary.formatters.abstract_formatter import AbstractFormatter


class CurrencyFormatter(AbstractFormatter):

    @staticmethod
    def format(schema_answers, state_answers, user_answer):
        return "£{:,}".format(user_answer)

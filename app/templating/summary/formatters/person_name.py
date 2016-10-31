from app.templating.summary.formatters.abstract_formatter import AbstractFormatter


class PersonNameFormatter(AbstractFormatter):

    @staticmethod
    def format(schema_answers, state_answers, user_answer):
        person_name = user_answer['person']
        return ' '.join([person_name['first'], person_name['middle'], person_name['last']])

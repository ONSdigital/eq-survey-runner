from app.templating.summary.formatters.abstract_formatter import AbstractFormatter


class PersonNameFormatter(AbstractFormatter):

    @staticmethod
    def format(schema_answers, state_answers, user_answer):
        key = [key if key.startswith('person') else '' for key in user_answer][0] if user_answer else ''
        person_name = user_answer[key]
        return ' '.join([person_name['first'], person_name['middle'], person_name['last']])

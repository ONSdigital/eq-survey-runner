import logging

from app.templating.summary.formatter_registry import FormatterRegistry

logger = logging.getLogger(__name__)


class SummaryItem(object):
    def __init__(self, schema, state_answers, question_type):
        self.schema = schema
        self.state_answers = state_answers
        self.question_type = question_type
        self.answer = self.format_answer()
        self.question = schema.title or schema.answers[0].label
        # Frontend url for each question
        self.link = schema.container.container.id + '#' + schema.answers[0].id
        self.type = self.schema.answers[0].type.lower()

    # Formatting the answer for the frontend e.g. currency needs £
    def format_answer(self):

        user_answer = self.state_answers[0].value

        if user_answer is not None:
            answer_type = self.schema.answers[0].type

            # find out if the question type and answer has a formatter
            formatter_class = FormatterRegistry.get_formatter(self.question_type, answer_type)
            if formatter_class:
                logger.debug("formatting answer %s", user_answer)
                formatter = formatter_class()
                return formatter.format(self.schema.answers, self.state_answers, user_answer)

            # Not all question/answer types need formatting
            return user_answer

        return None

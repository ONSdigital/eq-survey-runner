from app.templating.summary.formatter_registry import FormatterRegistry


class SummarySubItem:
    def __init__(self, schema, state_answers, question_type, answer):
        answer_schema = schema.questionnaire.get_item_by_id(answer.id)
        self.schema = schema
        self.state_answers = state_answers
        self.answer_title = answer_schema.label if not question_type == 'HOUSEHOLD' else \
            SummarySubItem.get_household_answer_title(answer)
        self.link = schema.container.container.id + '#' + answer.id
        self.type = answer_schema.type.lower()
        self.answer = self.format_answer(answer, question_type)

    @staticmethod
    def get_household_answer_title(answer):
        person_key = [k for k in answer.input][0].title()
        next_number = int(person_key[-1:]) + 1 if person_key[-1:].isdigit() else 1
        return SummarySubItem._get_person_label(next_number)

    @staticmethod
    def _get_person_label(number):
        return ' '.join(['Person', str(number)])

    # Formatting the answer for the frontend e.g. currency needs £
    def format_answer(self, answer, question_type):
        user_answer = answer.value

        if user_answer is not None:
            # find out if the question type and answer has a formatter
            formatter = FormatterRegistry.get_formatter(question_type, self.type)
            if formatter:
                return formatter.format(self.schema.answers, self.state_answers, user_answer)

            # Not all question/answer types need formatting
            return user_answer

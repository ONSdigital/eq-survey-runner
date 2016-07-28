from app.schema.answer import Answer
from app.validation.positive_integer_type_check import PositiveIntegerTypeCheck
from app.schema.widgets.text_widget import TextWidget


class PositiveIntegerAnswer(Answer):
    def __init__(self, answer_id=None):
        super().__init__(answer_id)
        self.type_checkers.append(PositiveIntegerTypeCheck())
        self.widget = TextWidget(self.id)

    def _cast_user_input(self, user_input):
        return int(user_input)

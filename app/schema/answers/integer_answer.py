from app.schema.answer import Answer
from app.schema.widgets.text_widget import TextWidget
from app.validation.integer_type_check import IntegerTypeCheck


class IntegerAnswer(Answer):
    def __init__(self, answer_id=None):
        super().__init__(answer_id)
        self.type_checkers.append(IntegerTypeCheck())
        self.widget = TextWidget(self.id)

    @staticmethod
    def _cast_user_input(user_input):
        return int(user_input)

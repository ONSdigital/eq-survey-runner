from app.schema.answer import Answer
from app.schema.widgets.textarea_widget import TextareaWidget
from app.validation.textarea_type_check import TextAreaTypeCheck


class TextareaAnswer(Answer):
    def __init__(self, answer_id=None):
        super().__init__(answer_id)
        self.type_checkers.append(TextAreaTypeCheck())
        self.widget = TextareaWidget(self.id)

    @staticmethod
    def _cast_user_input(user_input):
        return str(user_input)

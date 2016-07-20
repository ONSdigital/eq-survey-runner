from app.schema.answer import Answer
from app.validation.textarea_type_check import TextAreaTypeCheck


class TextareaAnswer(Answer):
    def __init__(self):
        super().__init__()
        self.type_checkers.append(TextAreaTypeCheck())

    def _cast_user_input(self, user_input):
        return str(user_input)

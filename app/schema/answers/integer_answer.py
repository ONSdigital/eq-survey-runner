from app.schema.answer import Answer
from app.validation.positive_integer_type_check import PositiveIntegerTypeCheck
from app.validation.integer_type_check import IntegerTypeCheck


class IntegerAnswer(Answer):
    def __init__(self):
        super().__init__()
        self.type_checkers.append(IntegerTypeCheck())

    def _cast_user_input(self, user_input):
        return int(user_input)


class PositiveIntegerAnswer(Answer):
    def __init__(self):
        super().__init__()
        self.type_checkers.append(PositiveIntegerTypeCheck())

    def _cast_user_input(self, user_input):
        return int(user_input)

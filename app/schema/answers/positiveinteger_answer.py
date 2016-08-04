from app.schema.answers.integer_answer import IntegerAnswer
from app.validation.positive_integer_type_check import PositiveIntegerTypeCheck


class PositiveIntegerAnswer(IntegerAnswer):
    def __init__(self, answer_id=None):
        super().__init__(answer_id)
        self.type_checkers.append(PositiveIntegerTypeCheck())

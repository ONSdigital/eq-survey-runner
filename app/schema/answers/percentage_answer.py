from app.schema.answer import Answer
from app.schema.widgets.percentage_widget import PercentageWidget
from app.validation.percentage_type_check import PercentageTypeCheck


class PercentageAnswer(Answer):
    def __init__(self, answer_id=None):
        super().__init__(answer_id)
        self.widget = PercentageWidget(self.id)
        self.type_checkers.append(PercentageTypeCheck())

    @staticmethod
    def _cast_user_input(user_input):
        return int(user_input)

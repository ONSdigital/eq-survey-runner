from app.schema.answer import Answer
from app.schema.widgets.text_widget import TextWidget


class PercentageAnswer(Answer):
    def __init__(self, answer_id=None):
        super().__init__(answer_id)
        self.widget = TextWidget(self.id)

    @staticmethod
    def _cast_user_input(user_input):
        return float(user_input)

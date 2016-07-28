from app.schema.answer import Answer
from app.schema.widgets.radio_group_widget import RadioGroupWidget


class RadioAnswer(Answer):
    def __init__(self, answer_id=None):
        super().__init__(answer_id)
        self.widget = RadioGroupWidget(self.id)

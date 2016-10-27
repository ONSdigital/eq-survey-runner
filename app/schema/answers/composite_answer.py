from app.schema.answer import Answer
from app.schema.widgets.composite_widget import CompositeWidget


class CompositeAnswer(Answer):

    def __init__(self, answer_id=None, answers=None, widgets=None):
        super(CompositeAnswer, self).__init__(answer_id)
        self.widget = CompositeWidget(name=self.id, widgets=widgets)
        self.answers = answers

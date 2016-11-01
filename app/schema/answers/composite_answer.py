from app.schema.answer import Answer
from app.schema.widgets.composite_widget import CompositeWidget


class CompositeAnswer(Answer):

    def __init__(self, answer_id=None):
        super(CompositeAnswer, self).__init__(answer_id)
        self.answers = None
        self.widget = None

    def add_children(self, answers=None):
        self.answers = answers
        self.widget = CompositeWidget(name=self.id, widgets=[answer.widget for answer in answers])

    def get_user_input(self, post_vars, index=0):
        return self.widget.get_user_input(post_vars, index)

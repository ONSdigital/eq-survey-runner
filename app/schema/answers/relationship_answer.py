from app.schema.answer import Answer
from app.schema.widgets.relationship_widget import RelationshipWidget


class RelationshipAnswer(Answer):
    def __init__(self, answer_id=None):
        super().__init__(answer_id)
        self.widget = RelationshipWidget(self.id)

from app.questionnaire_state.relationship_state_question import RelationshipStateQuestion
from app.schema.question import Question


class RelationshipQuestion(Question):
    def __init__(self):
        super().__init__()

    def get_state_class(self):
        return RelationshipStateQuestion

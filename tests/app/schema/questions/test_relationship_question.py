from unittest import TestCase

from app.questionnaire_state.relationship_state_question import RelationshipStateQuestion
from app.schema.questions.relationship_question import RelationshipQuestion


class TestRelationshipQuestion(TestCase):

    def test_state_class_should_be_relationship_state_question(self):
        # Given
        question = RelationshipQuestion()

        # When
        state_class = question.get_state_class()

        # Then
        self.assertEqual(state_class, RelationshipStateQuestion)

from unittest import TestCase

from app.schema.answers.relationship_answer import RelationshipAnswer
from app.schema.widgets.relationship_widget import RelationshipWidget


class TestRelationshipAnswer(TestCase):

    def test_widget_should_be_relationship_widget(self):
        # Given
        answer = RelationshipAnswer()

        # When
        widget = answer.widget

        # Then
        self.assertEqual(type(widget), RelationshipWidget)

    def test_widget_id_should_be_set(self):
        # Given
        answer = RelationshipAnswer('widget_id')

        # When
        widget = answer.widget

        # Then
        self.assertEqual(widget.id, 'widget_id')

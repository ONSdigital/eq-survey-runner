from unittest import TestCase

from mock import MagicMock

from app.schema.widget import Widget


class TestWidget(TestCase):

    def test_get_id_returns_schema_id_when_first_instance(self):
        # Given
        widget = Widget('answer-name')
        state = MagicMock()
        state.schema_item.id = 'answer-id'
        state.answer_instance = 0

        # When
        widget_id = widget.get_id(state)

        # Then
        self.assertEqual(widget_id, 'answer-id')

    def test_get_id_returns_id_with_instance_suffix(self):
        # Given
        widget = Widget('answer-name')
        state = MagicMock()
        state.schema_item.id = 'answer-id'
        state.answer_instance = 1

        # When
        widget_id = widget.get_id(state)

        # Then
        self.assertEqual(widget_id, 'answer-id_1')

        # Given
        widget = Widget('answer-name')
        state = MagicMock()
        state.schema_item.id = 'answer-id'
        state.answer_instance = 2

        # When
        widget_id = widget.get_id(state)

        # Then
        self.assertEqual(widget_id, 'answer-id_2')

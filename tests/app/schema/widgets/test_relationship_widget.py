from unittest import TestCase

from mock import patch, call

from app.questionnaire_state.state_answer import StateAnswer
from app.schema.answer import Answer
from app.schema.widgets.relationship_widget import RelationshipWidget


class TestRelationshipWidget(TestCase):

    def test_widget_should_contain_current_person(self):
        # Given
        widget = RelationshipWidget('relationship')
        widget.current_person = 'John Doe'
        state_answer = StateAnswer('who-related', Answer())

        # When
        widget_params = widget.build_widget_params(state_answer)

        # Then
        self.assertEqual(widget_params['answer']['current_person'], 'John Doe')

    def test_widget_should_contain_other_person(self):
        # Given
        widget = RelationshipWidget('relationship')
        widget.other_person = 'Jane Doe'
        state_answer = StateAnswer('who-related', Answer())

        # When
        widget_params = widget.build_widget_params(state_answer)

        # Then
        self.assertEqual(widget_params['answer']['other_person'], 'Jane Doe')

    def test_widget_should_contain_options(self):
        # Given
        widget = RelationshipWidget('relationship')
        answer = Answer()
        answer.options = [{'label': 'Husband or wife', 'value': 'Husband or wife'}, {'label': 'Son or daughter', 'value': 'Son or daughter'}]
        state_answer = StateAnswer('who-related', answer)

        # When
        widget_params = widget.build_widget_params(state_answer)

        # Then
        self.assertEqual(widget_params['widget']['options'][0].label, 'Husband or wife')
        self.assertEqual(widget_params['widget']['options'][0].value, 'Husband or wife')
        self.assertEqual(widget_params['widget']['options'][0].selected, False)
        self.assertEqual(widget_params['widget']['options'][1].label, 'Son or daughter')
        self.assertEqual(widget_params['widget']['options'][1].value, 'Son or daughter')
        self.assertEqual(widget_params['widget']['options'][0].selected, False)

    def test_widget_should_be_selected(self):
        # Given
        widget = RelationshipWidget('relationship')
        answer = Answer()
        answer.options = [{'label': 'Husband or wife', 'value': 'Husband or wife'},
                          {'label': 'Son or daughter', 'value': 'Son or daughter'}]
        state_answer = StateAnswer('who-related', answer)
        state_answer.input = 'Husband or wife'

        # When
        widget_params = widget.build_widget_params(state_answer)

        # Then
        self.assertEqual(widget_params['widget']['options'][0].selected, True)

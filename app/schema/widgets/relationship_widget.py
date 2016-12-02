from app.libs.utils import ObjectFromDict
from app.schema.widgets.multiple_choice_widget import MultipleChoiceWidget

from flask import render_template


class RelationshipWidget(MultipleChoiceWidget):
    def __init__(self, name):
        super().__init__(name)
        self.type = 'relationship'
        self.current_person = None
        self.other_person = None

    def render(self, answer_state):
        widget_params = self.build_widget_params(answer_state)
        return render_template('/partials/widgets/relationship_widget.html', **widget_params)

    def build_widget_params(self, answer_state):
        options = answer_state.schema_item.options or []
        widget_params = {
            'widget': {
                'options': self._build_options(options, answer_state.input),
                'type': self.type,
            },
            'answer': {
                'name': self.name,
                'id': self.id,
                'label': answer_state.schema_item.label,
                'current_person': self.current_person or '',
                'other_person': self.other_person or '',
            },
        }
        return widget_params

    @staticmethod
    def _build_options(schema_options, input_value):
        options = []

        for option in schema_options:
            radio_option = {
                'value': option['value'],
                'label': option['label'],
                'selected': option['value'] == input_value,
            }
            options.append(ObjectFromDict(radio_option))

        return options

import logging

from app.libs.utils import ObjectFromDict
from app.schema.widget import Widget

from flask import render_template

logger = logging.getLogger(__name__)


class RadioGroupWidget(Widget):
    def render(self, answer_state):
        widget_params = {
            'widget': {
                'options': self._build_options(answer_state.schema_item, answer_state),
                'allow_other': False,
            },
            'answer': {
                'name': self.name,
                'id': answer_state.schema_item.id + '-input',
                'label': answer_state.schema_item.label or 'Label',
            },
            'debug': {
                'state': answer_state.__dict__,
            },
        }

        return render_template('partials/widgets/radio_group_widget.html', **widget_params)

    def _build_options(self, answer_schema, answer_state):
        options = []

        if answer_schema.options:
            for option in answer_schema.options:
                options.append(ObjectFromDict({
                    'value': option['value'],
                    'label': option['label'],
                    'selected': option['value'] == answer_state.input,
                }))

        return options

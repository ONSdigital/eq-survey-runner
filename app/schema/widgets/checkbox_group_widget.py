from app.schema.widget import Widget
from flask import render_template
from app.libs.utils import ObjectFromDict
import logging

logger = logging.getLogger(__name__)


class CheckboxGroupWidget(Widget):
    def get_user_input(self, post_vars):
        # Returns an empty list
        return post_vars.getlist(self.name)

    def render(self, answer_state):
        widget_params = {
            'widget': {
                'options': self._build_options(answer_state.schema_item, answer_state)
            },
            'answer': {
                'name': self.name,
                'id': answer_state.schema_item.id,
                'label': answer_state.schema_item.label or 'Label'
            },
            'debug': {
                'state': answer_state.__dict__
            }
        }

        return render_template('/partials/widgets/checkbox_group_widget.html', **widget_params)

    def _build_options(self, answer_schema, answer_state):
        options = []

        if answer_schema.options:
            for option in answer_schema.options:
                option_selected = False
                if answer_state.input:
                    option_selected = option['value'] in answer_state.input
                options.append(ObjectFromDict({
                    'value': option['value'],
                    'label': option['label'],
                    'selected': option_selected
                }))

        return options

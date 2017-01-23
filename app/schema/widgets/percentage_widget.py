import logging

from flask import render_template

from app.schema.widget import Widget

logger = logging.getLogger(__name__)


class PercentageWidget(Widget):
    def render(self, state):
        widget_params = {
            'answer': {
                'name': self.name,
                'id': self.id,
                'label': state.schema_item.label,
                'description': state.schema_item.description,
                'value': state.value if state.value is not None else '',
            },
        }
        return render_template('partials/widgets/percentage_widget.html', **widget_params)

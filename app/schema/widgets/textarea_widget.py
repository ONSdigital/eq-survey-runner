import logging

from app.schema.widget import Widget

from flask import render_template

logger = logging.getLogger(__name__)


class TextareaWidget(Widget):
    def render(self, state):
        widget_params = {
            'answer': {
                'name': self.name,
                'id': self.id,
                'label': state.schema_item.label,
                'value': state.input or '',
            },
            'question': {
                'id': state.schema_item.container.id,
            },
        }
        return render_template('partials/widgets/textarea_widget.html', **widget_params)

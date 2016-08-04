from app.schema.widget import Widget
from flask import render_template
import logging

logger = logging.getLogger(__name__)


class TextWidget(Widget):
    def render(self, schema, state):
        widget_params = {
            'answer': {
                'name': self.name,
                'id': schema.id,
                'label': schema.label or '',
                'value': state.input or '',
                'placeholder': ''
            }
        }
        return render_template('partials/widgets/text_widget.html', **widget_params)

from app.schema.widget import Widget
from flask import render_template
import logging

logger = logging.getLogger(__name__)


class TextWidget(Widget):
    def render(self, state):
        widget_params = {
            'answer': {
                'name': self.name,
                'id': state.schema_item.id,
                'label': state.schema_item.label or '',
                'value': state.value or state.input or '',
                'placeholder': ''
            }
        }
        return render_template('partials/widgets/text_widget.html', **widget_params)

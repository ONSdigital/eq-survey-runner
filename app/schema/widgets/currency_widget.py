from app.schema.widget import Widget
from flask import render_template
import logging

logger = logging.getLogger(__name__)


class CurrencyWidget(Widget):
    def render(self, schema, state):
        widget_params = {
            'answer': {
                'name': self.name,
                'id': schema.id,
                'label': schema.label,
                'value': state.input,
                'placeholder': ''
            },
            'debug': {
                'schema': schema,
                'state': state
            }
        }
        return render_template('partials/widgets/currency_widget.html', **widget_params)

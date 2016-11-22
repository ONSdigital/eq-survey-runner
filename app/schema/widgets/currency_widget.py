import logging

from app.schema.widget import Widget

from flask import render_template

logger = logging.getLogger(__name__)


class CurrencyWidget(Widget):
    def render(self, state):
        widget_params = {
            'answer': {
                'name': self.name,
                'id': self.id,
                'label': state.schema_item.label,
                'value': state.value if state.value is not None else '',
                'placeholder': '',
            },
            'debug': {
                'schema': state.schema_item,
                'state': state,
            },
        }
        return render_template('partials/widgets/currency_widget.html', **widget_params)

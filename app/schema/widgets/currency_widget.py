import logging

from app.schema.widget import Widget

from flask import render_template, render_template_string

logger = logging.getLogger(__name__)


class CurrencyWidget(Widget):
    @staticmethod
    def get_template_string(params):
        return render_template_string(render_template('partials/widgets/currency_widget.html', **params))

    def render(self, state):
        widget_params = {
            'answer': {
                'name': self.name,
                'id': state.schema_item.id,
                'label': state.schema_item.label,
                'value': state.value or state.input or '',
                'placeholder': ''
            },
            'debug': {
                'schema': state.schema_item,
                'state': state,
            },
        }
        return render_template('partials/widgets/currency_widget.html', **widget_params)

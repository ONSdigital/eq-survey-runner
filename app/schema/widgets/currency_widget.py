from app.schema.widget import Widget
from flask import render_template
import logging

logger = logging.getLogger(__name__)


class CurrencyWidget(Widget):
    def __init__(self, name):
        super().__init__(name)

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

    def get_user_input(self, post_vars):
        logger.debug('Getting user input for: ' + self.name)
        return post_vars.get(self.name, None)

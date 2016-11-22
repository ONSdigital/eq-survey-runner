import logging

from app.schema.widget import Widget

from flask import render_template

logger = logging.getLogger(__name__)


class TextWidget(Widget):
    def render(self, state):
        widget_params = {
            'answer': {
                'name': self.name,
                'id': self.id,
                'label': state.schema_item.label or '',
                'value': state.value if state.value is not None else '',
            },
        }
        return render_template('partials/widgets/text_widget.html', **widget_params)

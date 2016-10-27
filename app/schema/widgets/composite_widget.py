import logging

from app.schema.widget import Widget

from flask import render_template, render_template_string

logger = logging.getLogger(__name__)


class CompositeWidget(Widget):

    def __init__(self, name=None, widgets=None):
        super(CompositeWidget, self).__init__(name)
        self.widgets = widgets

    def render(self, state):
        composite_widget = None
        widget_params = {
            'answer': {
                'name': self.name,
                'id': state.schema_item.id,
                'label': state.schema_item.label,
                'value': state.input or '',
            },
            'question': {
                'id': state.schema_item.container.id,
            },
        }
        return render_template('partials/widgets/composite_widget.html', **widget_params)

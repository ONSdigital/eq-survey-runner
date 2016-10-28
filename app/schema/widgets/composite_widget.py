import logging

from app.schema.widget import Widget

logger = logging.getLogger(__name__)


class CompositeWidget(Widget):

    def __init__(self, name=None, widgets=None):
        super(CompositeWidget, self).__init__(name)
        self.widgets = widgets

    def render(self, state):

        composite_template = ''
        for index, widget in enumerate(self.widgets):
            widget_params = self.__create_widget_params(state, index)
            composite_template = composite_template + widget.get_template_string(widget_params)

        return composite_template

    def __create_widget_params(self, state, index):
        widget_params = {
            'answer': {
                'name': self.name,
                'id': ''.join([state.schema_item.answers[index].id, '-',  str(index)]),
                'label': state.schema_item.answers[index].label,
                'value': state.input or '',
            },
            'question': {
                'id': state.schema_item.container.id,
            },
        }
        return widget_params

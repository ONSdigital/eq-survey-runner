import logging

from app.schema.widget import Widget

logger = logging.getLogger(__name__)


class CompositeWidget(Widget):

    def __init__(self, name=None, widgets=None):
        super(CompositeWidget, self).__init__(name)
        self.widgets = widgets
        self._index = 0

    def render(self, state):
        composite_template = ''
        for index, widget in enumerate(self.widgets):
            widget_params = self._create_widget_params(state, index)
            composite_template = composite_template + widget.get_template_string(widget_params)

        return composite_template

    def get_user_input(self, post_vars):
        user_input = post_vars.get(self.name, None)
        logger.debug('Getting user input for "{}", value is "{}"'.format(self.name, user_input))
        return user_input

    def _create_widget_params(self, state, index):
        widget_params = {
            'answer': {
                'name': ''.join([self.name, '-', str(self._index), '-', self.widgets[index].name]),
                'id': state.schema_item.answers[index].id,
                'label': state.schema_item.answers[index].label,
                'value': state.input or '',
            },
            'question': {
                'id': state.schema_item.container.id,
            },
        }
        return widget_params

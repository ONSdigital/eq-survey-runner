import ast
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
            widget_params = self._create_widget_params(state, index)
            composite_template = composite_template + widget.get_template_string(widget_params)

        return composite_template

    def get_user_input(self, post_vars):

        if post_vars is None or len(post_vars) == 0:
            return None

        is_post = True
        data = post_vars
        if not hasattr(post_vars, 'getlist'):
            # During GET post_vars is a dict that we need to unpack.
            data = ast.literal_eval(post_vars[self.name])[self.name]
            is_post = False

        widget_input = {}
        for child_widget in self.widgets:
            key = self.name + '-' + child_widget.name if is_post else child_widget.name
            widget_input[child_widget.name] = data.get(key)

        return {self.name: widget_input}

    def _create_widget_params(self, state, index):
        widget_params = {
            'answer': {
                'name': ''.join([self.name, '-', self.widgets[index].name]),
                'id': state.schema_item.answers[index].id,
                'label': state.schema_item.answers[index].label,
                'value': state.input['person'][self.widgets[index].name] if state.input is not None else '',
            },
            'question': {
                'id': state.schema_item.container.id,
            },
        }
        return widget_params

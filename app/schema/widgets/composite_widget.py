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

    def get_user_input(self, post_vars, index=0):

        if post_vars is None or len(post_vars) == 0:
            return None

        is_post = True
        data = post_vars
        if not hasattr(post_vars, 'getlist'):
            # During GET post_vars is a dict that we need to unpack.
            key = self._get_key_name(index)
            data = ast.literal_eval(post_vars[key])[key]
            is_post = False

        widget_input = {}
        for child_widget in self.widgets:
            key = self._get_key_name(index) + '-' + child_widget.name if is_post else child_widget.name
            widget_input[child_widget.name] = data.get(key)

        return {self._get_key_name(index): widget_input}

    def _get_key_name(self, index):
        return self.name if index == 0 else self.name + str(index)

    def _create_widget_params(self, state, widget_offset):
        person_key = [key if key.startswith('person') else '' for key in state.input][0] if state.input else self.name
        widget_params = {
            'answer': {
                'name': '-'.join([person_key, self.widgets[widget_offset].name]),
                'id': state.schema_item.answers[widget_offset].id,
                'label': state.schema_item.answers[widget_offset].label,
                'value': state.input[person_key][self.widgets[widget_offset].name] if state.input is not None else '',
            },
            'question': {
                'id': state.schema_item.container.id,
            },
        }
        return widget_params

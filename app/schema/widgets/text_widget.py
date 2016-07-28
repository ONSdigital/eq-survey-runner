from app.schema.widget import Widget
from flask import render_template


class TextWidget(Widget):
    def __init__(self, name):
        super().__init__(name)

    def render(self, schema, state):
        widget_params = {
            'answer': {
                'name': self.name,
                'id': schema.id,
                'label': schema.label or '',
                'value': state.input or '',
                'placeholder': ''
            }
        }
        return render_template('partials/widgets/text_widget.html', **widget_params)

    def get_user_input(self, post_vars):
        return post_vars.get(self.name, None)

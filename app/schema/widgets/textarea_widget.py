from app.schema.widget import Widget
from flask import render_template


class TextareaWidget(Widget):
    def __init__(self, name):
        super().__init__(name)

    def render(self, schema, state):
        widget_params = {
            'answer': {
                'name': self.name,
                'id': schema.id,
                'label': schema.label,
                'value': state.input or '',
                'placeholder': '',
                'maxChars': 2000
            },
            'question': {
                'id': schema.container.id
            }
        }
        return render_template('partials/widgets/textarea_widget.html', **widget_params)

    def get_user_input(self, post_vars):
        return post_vars.get(self.name, None)

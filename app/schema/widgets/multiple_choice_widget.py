import logging

from app.schema.widget import Widget

from flask import render_template

logger = logging.getLogger(__name__)


class MultipleChoiceWidget(Widget):

    def render(self, answer_state):
        widget_params = {
            'widget': {
                'options': self._build_options(answer_state.schema_item, answer_state),
                'type': self.type,
            },
            'answer': {
                'name': self.name,
                'id': answer_state.schema_item.id,
                'label': answer_state.schema_item.label or 'Label',
            },
            'debug': {
                'state': answer_state.__dict__,
            },
        }

        return render_template('/partials/widgets/multiple_choice_widget.html', **widget_params)

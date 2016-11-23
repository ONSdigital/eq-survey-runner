import logging

from abc import ABCMeta, abstractmethod

from app.schema.widget import Widget

from flask import render_template

logger = logging.getLogger(__name__)


class MultipleChoiceWidget(Widget, metaclass=ABCMeta):

    def __init__(self, name="MultipleChoiceWidget"):
        """
        self.type must be defined by derived classes
        """
        super().__init__(name)
        self.type = None

    @staticmethod
    @abstractmethod
    def _build_options(schema_item, answer_state):
        raise NotImplementedError

    def render(self, answer_state):
        widget_params = {
            'widget': {
                'options': self._build_options(answer_state.schema_item, answer_state),
                'type': self.type,
            },
            'answer': {
                'name': self.name,
                'id': self.id,
                'label': answer_state.schema_item.label or 'Label',
            },
            'debug': {
                'state': answer_state.__dict__,
            },
        }

        return render_template('/partials/widgets/multiple_choice_widget.html', **widget_params)

    def get_other_input(self, post_vars):
        """
        Depending on which part of the processing is being done, POST or GET, this post_vars
        passed to this method can either be an ImmutableMultiDict or a plain dict object.
        :param post_vars:
        :return: The other input value, if present, 'Other' if other selected but no value, or None.
        """
        if len(post_vars) == 0:
            return None

        is_immutable_multi_dict = hasattr(post_vars, 'getlist')
        posted_data = post_vars.getlist(self.name) if is_immutable_multi_dict else post_vars.get(self.name)

        has_multiple_values = isinstance(posted_data, list) and len(posted_data) > 1

        is_other_selected = str(posted_data[:1][0]).strip().lower() == 'other' if has_multiple_values else False

        other_value = str(posted_data[-1:][0]).strip() if is_other_selected else None

        return other_value if other_value is not None and len(other_value) > 0 else None

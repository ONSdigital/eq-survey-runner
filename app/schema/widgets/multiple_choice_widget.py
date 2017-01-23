import logging
from abc import ABCMeta, abstractmethod

from flask import render_template

from app.helpers.multiple_choice_helper import MultipleChoiceHelper
from app.schema.widget import Widget

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
                'label': answer_state.schema_item.label,
                'description': answer_state.schema_item.description,
            },
            'debug': {
                'state': answer_state.__dict__,
            },
        }

        return render_template('/partials/widgets/multiple_choice_widget.html', **widget_params)

    def get_other_input(self, post_vars, options):
        """
        Depending on which part of the processing is being done, POST or GET, this post_vars
        passed to this method can either be an ImmutableMultiDict or a plain dict object.
        :param post_vars:
        :return: The other input value, if present, 'Other' if other selected but no value, or None.
        """

        if hasattr(post_vars, 'getlist'):
            posted_data = post_vars.getlist(self.name)
        else:
            posted_data = post_vars.get(self.name)

        return MultipleChoiceHelper.find_other_value(posted_data, options)

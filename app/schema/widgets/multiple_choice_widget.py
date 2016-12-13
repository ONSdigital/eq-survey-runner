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

        return self.find_other_value(posted_data, options)

    @staticmethod
    def find_other_value(posted_data, options):
        """
        Compare the posted_data with the options in the schema, if there is a value which doesn't match
        the options it must be the other value
        """
        if posted_data and 'other' in (value.lower() for value in posted_data):
            for answer in posted_data:
                answer_in_options = any(option['value'] == answer for option in options)
                if answer and not answer.isspace() and not answer_in_options and answer.lower() != 'other':
                    return answer

        return None

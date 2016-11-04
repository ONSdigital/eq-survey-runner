from app.libs.utils import ObjectFromDict

from app.schema.widgets.multiple_choice_widget import MultipleChoiceWidget

from werkzeug.datastructures import ImmutableMultiDict


class CheckboxGroupWidget(MultipleChoiceWidget):

    def __init__(self, name):
        super().__init__(name)
        self.type = 'checkbox'

    def get_user_input(self, post_vars):

        if isinstance(post_vars, dict):
            return ImmutableMultiDict(post_vars).getlist(self.name)

        return post_vars

    def _build_options(self, answer_schema, answer_state):
        options = []

        if answer_schema.options:
            for option in answer_schema.options:
                option_selected = False
                if answer_state.input:
                    option_selected = option['value'] in answer_state.input

                checkbox_option = {
                    'value': option['value'],
                    'label': option['label'],
                    'selected': option_selected,
                    'other': option['other'] if 'other' in option else None,
                    'other_value': answer_state.other if hasattr(answer_state, 'other') else None,
                }

                if 'description' in option:
                    checkbox_option['description'] = option['description']

                options.append(ObjectFromDict(checkbox_option))

        return options

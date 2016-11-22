import logging

from app.questionnaire_state.exceptions import StateException
from app.schema.answer import Answer
from app.schema.widgets.checkbox_group_widget import CheckboxGroupWidget

logger = logging.getLogger(__name__)


class CheckboxAnswer(Answer):
    def __init__(self, answer_id=None):
        super().__init__(answer_id)
        self.widget = CheckboxGroupWidget(self.id)

    def get_typed_value(self, post_vars):
        # We cannot type cast a list of values, so just return the user_input
        return self.get_user_input(post_vars)

    def validate(self, state):
        if isinstance(state, self.get_state_class()):
            question = state.parent
            options = state.schema_item.options
            logger.debug("Checkbox Question is skipped %s", question.skipped)
            # Mandatory check

            if question.skipped:
                state.is_valid = True
            elif self.mandatory:
                if not state.input:
                    super(CheckboxAnswer, self).mandatory_error(state)
                elif 'other' not in state.input and not self._valid_option_selected(state.input, options):
                    super(CheckboxAnswer, self).mandatory_error(state)
                elif 'other' in state.input and not self.widget.find_other_value(state.input, options):
                    super(CheckboxAnswer, self).mandatory_error(state)

            # Here we just report on whether the answer has passed type checking
            state.value = self.get_typed_value(state.input)

            return state.is_valid
        else:
            raise StateException('Cannot validate - incorrect state class')

    @staticmethod
    def check_user_input(user_input):
        return user_input if (Answer.check_user_input(user_input) and
                              user_input != [''] and
                              user_input != [None]) else None

    @staticmethod
    def _valid_option_selected(state_input, options):
        # Check to see if the user input is one of the options in the schema
        valid_option_selected = False
        if state_input:
            for answer in state_input:
                if answer and any(option['value'] == answer for option in options) and answer != 'other':
                    valid_option_selected = True
                    break
        return valid_option_selected

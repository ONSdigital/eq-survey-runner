from app.schema.answer import Answer
from app.schema.widgets.checkbox_group_widget import CheckboxGroupWidget
from app.questionnaire_state.exceptions import StateException


class CheckboxAnswer(Answer):
    def __init__(self, answer_id=None):
        super().__init__(answer_id)
        self.widget = CheckboxGroupWidget(self.id)

    def get_typed_value(self, post_vars):
        # We cannot tyoe cast a list of values, so just return the user_input
        return self.get_user_input(post_vars)

    def get_user_input(self, post_vars):
        return self.widget.get_user_input(post_vars)

    def validate(self, state):
        if isinstance(state, self.get_state_class()):

            # Mandatory check
            if self.mandatory and len(state.input) == 0:
                state.errors = []
                state.errors.append(self.questionnaire.get_error_message('MANDATORY', self.id))
                state.is_valid = False
                return False

            # Here we just report on whether the answer has passed type checking
            return state.is_valid
        else:
            raise StateException('Cannot validate - incorrect state class')

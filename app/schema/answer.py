import logging

from app.questionnaire_state.answer import Answer as State
from app.questionnaire_state.exceptions import StateException
from app.schema.exceptions import TypeCheckingException
from app.schema.item import Item

import bleach

logger = logging.getLogger(__name__)


class Answer(Item):
    def __init__(self, answer_id=None):
        self.id = answer_id
        self.label = ""
        self.guidance = ""
        self.type = None
        self.code = None
        self.container = None
        self.mandatory = False
        self.validation = None
        self.questionnaire = None
        self.display = None
        self.messages = {}
        self.templatable_properties = []
        self.options = []
        self.alias = None
        self.type_checkers = []
        self.widget = None
        self.skip_condition = None

    def construct_state(self):
        return State(self.id, self)

    def get_state_class(self):
        return State

    def get_user_input(self, post_vars):
        user_input = self.widget.get_user_input(post_vars)
        return self._user_input_or_none_if_empty(user_input)

    def get_other_value(self, post_vars):
        """ Gets the value of the Other input field for a Radio or Checkbox

        :returns a str for the Other value or None"""
        if self.type == 'Radio' or self.type == 'Checkbox':
            user_input = self.widget.get_other_input(post_vars)
            return self._user_input_or_none_if_empty(user_input)

    @staticmethod
    def _user_input_or_none_if_empty(user_input):
        if user_input and not str(user_input).isspace() and user_input != '':
            return user_input
        else:
            return None

    def get_typed_value(self, post_vars):
        if self.id in post_vars.keys():
            user_input = bleach.clean(post_vars[self.id])

            for checker in self.type_checkers:
                result = checker.validate(user_input)
                if not result.is_valid:
                    raise TypeCheckingException(result.errors[0])

            return self._cast_user_input(user_input)
        else:
            return None

    def _cast_user_input(self, user_input):
        return user_input

    def validate(self, state):
        if isinstance(state, self.get_state_class()):
            question = state.parent
            if question.skipped:
                # if the question is skipped then its always valid
                state.is_valid = True
            elif self.mandatory and state.input is None:
                self.mandatory_error(state)
            elif self.mandatory and self.type == 'Radio' and state.value == 'other' and state.input == 'other' and state.other is None:
                self.mandatory_error(state)

            # Here we just report on whether the answer has passed type checking
            return state.is_valid
        else:
            raise StateException('Cannot validate - incorrect state class')

    def mandatory_error(self, state):
        state.errors = []
        state.errors.append(self.questionnaire.get_error_message('MANDATORY', self.id))
        state.is_valid = False

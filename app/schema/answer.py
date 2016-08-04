from app.questionnaire_state.answer import Answer as State
from app.schema.exceptions import TypeCheckingException
from app.questionnaire_state.exceptions import StateException
from app.schema.item import Item
import bleach


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

    def construct_state(self):
        return State(self.id)

    def get_state_class(self):
        return State

    def get_user_input(self, post_vars):
        user_input = self.widget.get_user_input(post_vars)
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

            # Mandatory check
            if self.mandatory and state.input is None:
                state.errors = []
                state.errors.append(self.questionnaire.get_error_message('MANDATORY', self.id))
                state.is_valid = False
                return False

            # Here we just report on whether the answer has passed type checking
            return state.is_valid
        else:
            raise StateException('Cannot validate - incorrect state class')

    def augment_with_state(self, state):
        # These are her to avoid rebuilding the whole rendering pipeline
        self.state = state

        if state.id == self.id:
            self.is_valid = state.is_valid
            self.errors = state.errors
            self.warnings = state.warnings
            self.value = state.value
            self.input = state.input

    def _collect_property(self, property_name):
        collection = {}
        if hasattr(self, property_name):
            value = getattr(self, property_name)
            if value:
                collection[self.id] = value

        return collection

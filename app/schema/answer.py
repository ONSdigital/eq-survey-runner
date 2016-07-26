from app.questionnaire_state.answer import Answer as State
from app.schema.item import Item
import bleach


class Answer(Item):
    def __init__(self):
        self.id = None
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

    def construct_state(self):
        return State(self.id)

    def get_state_class(self):
        return State

    def get_typed_value(self, post_vars):
        if self.id in post_vars.keys():
            user_input = bleach.clean(post_vars[self.id])

            for checker in self.type_checkers:
                result = checker.validate(user_input)
                if not result.is_valid:
                    raise Exception(result.errors[0])

            return self._cast_user_input(user_input)
        else:
            return None

    def _cast_user_input(self, user_input):
        return user_input

    def validate(self, state):
        if isinstance(state, self.get_state_class()):
            # Here we just report on whether the answer has passed type checking
            return state.is_valid
        else:
            raise Exception('Cannot validate - incorrect state class')

    def augment_with_state(self, state):
        if state.id == self.id:
            self.is_valid = state.is_valid
            self.errors = state.errors
            self.warnings = state.warnings
            self.value = state.value
            self.input = state.input

    def _collect_property(self, property_name):
        collection = {}
        if hasattr(self, property_name):
            collection[self.id] = getattr(self, property_name)

        return collection


from app.questionnaire_state.state_item import StateItem


class StateAnswer(StateItem):
    def __init__(self, id, schema_item):
        super().__init__(id=id, schema_item=schema_item)
        # typed value
        self.value = None
        # actual user input
        self.input = None
        self.other = None

    def update_state(self, user_input):

        # Clear any previous value and validation results
        self.value = None
        self.is_valid = True
        self.errors = []
        # Get the user input
        # Todo, there shouldn't be a need for both self.input and self.value, but self.value gets changed later in the code
        self.input = self.schema_item.get_user_input(user_input)
        self.value = self.schema_item.get_user_input(user_input)
        self.other = self.schema_item.get_other_value(user_input)

    def get_answers(self):
        return [self]

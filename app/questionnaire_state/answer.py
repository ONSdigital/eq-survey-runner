from app.questionnaire_state.item import Item
from app.schema.exceptions import TypeCheckingException


class Answer(Item):
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
        self.input = self.schema_item.get_user_input(user_input)

        # Try and get the typed value
        if self.input:
            try:
                self.value = self.schema_item.get_typed_value(user_input)
                self.other = self.schema_item.get_other_value(user_input)
            except TypeCheckingException as e:
                self.is_valid = False
                self.errors = []
                self.errors.append(self.schema_item.questionnaire.get_error_message(str(e), self.id))

    def get_answers(self):
        return [self]

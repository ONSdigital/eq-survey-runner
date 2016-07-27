from app.questionnaire_state.item import Item


class Answer(Item):
    def __init__(self, id):
        super().__init__(id=id)
        # typed value
        self.value = None
        # actual user input
        self.input = None

    def update_state(self, user_input, schema_item):
        # Do we have the item or it's containing block?
        if schema_item.id != self.id:
            schema_item = schema_item.questionnaire.get_item_by_id(self.id)

        # Get the user input
        self.input = schema_item.get_user_input(user_input)

        # Mandatory check
        if schema_item.mandatory and self.input is None:
            self.errors = []
            self.errors.append(schema_item.questionnaire.get_error_message('MANDATORY', schema_item.id))
            self.is_valid = False

        # Try and get the typed value
        if self.input is not None:
            try:
                self.value = schema_item.get_typed_value(user_input)
                self.is_valid = True
                self.errors = None
                self.warnings = None
            except Exception as e:
                self.value = None
                # @TODO: Need to look again at this interface when we come to warnings
                self.errors = []
                self.errors.append(schema_item.questionnaire.get_error_message(str(e), schema_item.id))
                self.is_valid = False

    def get_answers(self):
        return [self]

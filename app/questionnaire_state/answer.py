from app.questionnaire_state.item import Item


class Answer(Item):
    def __init__(self, id):
        super().__init__(id=id)
        # typed value
        self.value = None
        # actual user input
        self.input = None

    def update_state(self, user_input, schema_item):
        if self.id in user_input.keys():
            self.input = user_input[self.id]
            if schema_item:
                try:
                    # Do we have the item or it's containing block?
                    if schema_item.id != self.id:
                        schema_item = schema_item.questionnaire.get_item_by_id(self.id)

                    # Mandatory check
                    if self.input:
                        self.value = schema_item.get_typed_value(user_input)
                        self.is_valid = True
                    elif schema_item.mandatory:
                        self.errors = []
                        self.errors.append(schema_item.questionnaire.get_error_message('MANDATORY', schema_item.id))
                        self.is_valid = False
                except Exception as e:
                    self.value = None
                    # @TODO: Need to look again at this interface when we come to warnings
                    self.errors = []
                    self.errors.append(schema_item.questionnaire.get_error_message(str(e), schema_item.id))
                    self.is_valid = False

    def get_answers(self):
        return [self]

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
        try:
            if schema_item:
                if schema_item.id == self.id:
                    self.value = schema_item.get_typed_value(user_input)
                else:
                    item = schema_item.questionnaire.get_item_by_id(self.id)
                    self.value = item.get_typed_value(user_input)
                self.is_valid = True
        except Exception as e:
            self.value = None
            # @TODO: Need to look again at this interface when we come to warnings
            self.errors = str(e)
            self.is_valid = False

    def get_answers(self):
        return [self]

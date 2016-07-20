from app.questionnaire_state.item import Item


class Answer(Item):
    def __init__(self, id):
        super().__init__(id=id)
        # typed value
        self.value = None
        # actual user input
        self.input = None

    def update_state(self, user_input):
        if self.id in user_input.keys():
            self.input = user_input[self.id]

    def get_answers(self):
        return [self]

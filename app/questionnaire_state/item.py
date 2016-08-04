

class Item(object):
    def __init__(self, id, schema_item):
        self.id = id
        self.children = []
        self.is_valid = None
        self.errors = []
        self.warnings = []
        self.schema_item = schema_item

    def update_state(self, user_input):
        for child in self.children:
            child.update_state(user_input)

    def get_answers(self):
        answers = []
        for child in self.children:
            answers.extend(child.get_answers())
        return answers

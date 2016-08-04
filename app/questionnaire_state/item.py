

class Item(object):
    def __init__(self, id):
        self.id = id
        self.sections = []
        self.children = []
        self.is_valid = None
        self.errors = None
        self.warnings = None

    def update_state(self, user_input, schema_item):
        for child in self.children:
            child.update_state(user_input, schema_item)

    def get_answers(self):
        answers = []
        for child in self.children:
            answers.extend(child.get_answers())
        return answers

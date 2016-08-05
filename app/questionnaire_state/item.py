

class Item(object):
    def __init__(self, id, schema_item):
        self.id = id
        self.children = []
        self.is_valid = None
        self.errors = []
        self.warnings = []
        self.schema_item = schema_item
        self.answers = {}

    def update_state(self, user_input):
        for child in self.children:
            child.update_state(user_input)

        # once state is updated collect answers
        self.answers = self._collect_answers()

    def _collect_answers(self):
        '''
        Collect answers into a dict keyed by id for quick look up
        '''
        answers_as_dict = {}
        answers = self.get_answers()
        for answer in answers:
            answers_as_dict[answer.id] = answer.input
        return answers_as_dict

    def get_answers(self):
        answers = []
        for child in self.children:
            answers.extend(child.get_answers())
        return answers

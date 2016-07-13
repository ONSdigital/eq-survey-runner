from app.questionnaire_state.answer import Answer


class Question(object):
    def __init__(self, id):
        self.id = id
        self.answers = []
        self.children = self.answers
        self.is_valid = None
        self.errors = None
        self.warnings = None

    def update_state(self, user_input):
        for child in self.children:
            child.update_state(user_input)

    @staticmethod
    def construct_state(item):
        state = Question(item.id)
        for child in item.children:
            child_state = Answer.construct_state(child)
            state.children.append(child_state)
        return state

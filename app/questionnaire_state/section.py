from app.questionnaire_state.question import Question


class Section(object):
    def __init__(self, id):
        self.id = id
        self.questions = []
        self.children = self.questions
        self.is_valid = None
        self.errors = None
        self.warnings = None

    def update_state(self, user_input):
        for child in self.children:
            child.update_state(user_input)

    @staticmethod
    def construct_state(item):
        state = Section(item.id)
        for child in item.children:
            child_state = Question.construct_state(child)
            state.children.append(child_state)
        return state

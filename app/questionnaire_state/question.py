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

    def get_answer(self, id):
        for child in self.children:
            answer = child.get_answer(id)
            if answer:
                return answer
        # haven't found anything so return none
        return None

    def get_answers(self):
        answers = []
        for child in self.children:
            answers.append(child.get_answer())
        return answers

    @staticmethod
    def construct_state(item):
        state = Question(item.id)
        for child in item.children:
            child_state = Answer.construct_state(child)
            state.children.append(child_state)
        return state

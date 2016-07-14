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
            answers.extend(child.get_answers())
        return answers

    @staticmethod
    def construct_state(item):
        state = Section(item.id)
        for child in item.children:
            child_state = Question.construct_state(child)
            state.children.append(child_state)
        return state

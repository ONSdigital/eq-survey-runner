from app.questionnaire_state.section import Section


class Block(object):

    def __init__(self, id):
        self.id = id
        self.sections = []
        self.children = self.sections
        self.is_valid = None
        self.errors = None
        self.warnings = None

    def update_state(self, user_input):
        for child in self.children:
            child.update_state(user_input)

    @staticmethod
    def construct_state(item):
        state = Block(item.id)
        for child in item.children:
            child_state = Section.construct_state(child)
            state.children.append(child_state)
        return state

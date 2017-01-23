from app.questionnaire_state.state_section import StateSection
from app.schema.item import Item


class Section(Item):
    def __init__(self, item_id=None):
        super().__init__(item_id)
        self.title = None
        self.number = None
        self.description = None
        self.questions = []
        self.children = self.questions
        self.container = None
        self.templatable_properties = ['title', 'description']

    def add_question(self, question):
        if question not in self.questions:
            self.questions.append(question)
            question.container = self

    def get_state_class(self):
        return StateSection

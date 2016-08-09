from app.schema.display import Display
from app.schema.item import Item
from app.questionnaire_state.section import Section as State


class Section(Item):
    def __init__(self):
        self.id = None
        self.title = None
        self.description = None
        self.questions = []
        self.children = self.questions
        self.container = None
        self.questionnaire = None
        self.validation = None
        self.questionnaire = None
        self.templatable_properties = ['title']
        self.display = Display()
        self.skip_condition = None

    def add_question(self, question):
        if question not in self.questions:
            self.questions.append(question)
            question.container = self

    def get_state_class(self):
        return State

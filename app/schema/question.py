from app.questionnaire_state.question import Question as State
from app.schema.display import Display
from app.schema.item import Item


class Question(Item):
    def __init__(self):
        self.id = None
        self.title = None
        self.description = ""
        self.answers = []
        self.children = self.answers
        self.container = None
        self.questionnaire = None
        self.validation = None
        self.questionnaire = None
        self.templatable_properties = ['title', 'description']
        self.display = Display()
        self.type = None
        self.messages = {}
        self.skip_condition = None

    def add_answer(self, answer):
        if answer not in self.answers:
            self.answers.append(answer)
            answer.container = self

    def get_state_class(self):
        return State

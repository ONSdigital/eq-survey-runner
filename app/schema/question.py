from app.questionnaire_state.state_question import StateQuestion
from app.schema.item import Item


class Question(Item):
    def __init__(self, item_id=None):
        super().__init__(item_id)
        self.title = None
        self.number = None
        self.description = ""
        self.guidance = None
        self.answers = []
        self.children = self.answers
        self.container = None
        self.templatable_properties = ['title', 'description', 'guidance']
        self.type = None
        self.messages = {}

    def add_answer(self, answer):
        if answer not in self.answers:
            self.answers.append(answer)
            answer.container = self

    def get_state_class(self):
        return StateQuestion

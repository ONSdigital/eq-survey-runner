from app.questionnaire_state.answer import Answer as State
from app.schema.item import Item


class Answer(Item):
    def __init__(self):
        self.id = None
        self.label = ""
        self.guidance = ""
        self.type = None
        self.code = None
        self.container = None
        self.mandatory = False
        self.validation = None
        self.questionnaire = None
        self.display = None
        self.messages = {}
        self.templatable_properties = []
        self.options = []
        self.alias = None

    def construct_state(self):
        return State(self.id)

    def get_state_class(self):
        return State

from app.questionnaire_state.state_block import StateBlock
from app.schema.display import Display
from app.schema.item import Item


class Block(Item):
    def __init__(self, id=None):
        super().__init__(id)
        self.type = None
        self.sections = []
        self.children = self.sections
        self.container = None
        self.questionnaire = None
        self.validation = None
        self.questionnaire = None
        self.templatable_properties = []
        self.display = Display()
        self.routing_rules = []
        self.skip_condition = None
        self.repetition = 1

    def add_section(self, section):
        if section not in self.sections:
            self.sections.append(section)
            section.container = self

    def get_state_class(self):
        return StateBlock

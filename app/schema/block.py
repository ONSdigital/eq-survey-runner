from app.schema.item import Item
from app.schema.display import Display
from app.questionnaire_state.block import Block as State


class Block(Item):
    def __init__(self):
        self.id = None
        self.title = None
        self.sections = []
        self.children = self.sections
        self.container = None
        self.questionnaire = None
        self.validation = None
        self.questionnaire = None
        self.templatable_properties = []
        self.display = Display()
        self.routing_rules = []

    def add_section(self, section):
        if section not in self.sections:
            self.sections.append(section)
            section.container = self

    def get_state_class(self):
        return State

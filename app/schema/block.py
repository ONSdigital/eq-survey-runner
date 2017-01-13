from app.questionnaire_state.state_block import StateBlock
from app.schema.item import Item


class Block(Item):
    def __init__(self, block_id=None):
        super().__init__(block_id)
        self.type = None
        self.sections = []
        self.children = self.sections
        self.container = None
        self.templatable_properties = []

    def add_section(self, section):
        if section not in self.sections:
            self.sections.append(section)
            section.container = self

    def get_state_class(self):
        return StateBlock

from app.model.display import Display


class Block(object):
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

    def add_section(self, section):
        if section not in self.sections:
            self.sections.append(section)
            section.container = self

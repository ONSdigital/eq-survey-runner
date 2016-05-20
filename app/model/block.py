class Block(object):
    def __init__(self):
        self.id = None
        self.title = None
        self.sections = []
        self.children = self.sections
        self.container = None
        self.questionnaire = None
        self.validation = None
        self.questionniare = None
        self.templatable_properties = []

    def add_section(self, section):
        if section not in self.sections:
            self.sections.append(section)
            section.container = self

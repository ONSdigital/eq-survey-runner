class Block(object):
    def __init__(self):
        self.id = None
        self.title = None
        self.sections = []

    def add_section(self, section):
        if section not in self.sections:
            self.sections.append(section)
            section.container = self

class Block(object):
    def __init__(self):
        self.id = None
        self.title = None
        self.sections = []
        self.container = None

    def add_section(self, section):
        if section not in self.sections:
            self.sections.append(section)
            section.container = self

    def get_item_by_id(self, id):
        if id == self.id:
            return self
        else:
            item = None
            for section in self.sections:
                candidate = section.get_item_by_id(id)
                if candidate is not None:
                    item = candidate
            return item

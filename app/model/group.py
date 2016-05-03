class Group(object):

    def __init__(self):
        self.id = None
        self.title = None
        self.blocks = []
        self.children = self.blocks
        self.container = None
        self.questionnaire = None
        self.validation = None
        self.questionnaire = None

    def add_block(self, block):
        if block not in self.blocks:
            self.blocks.append(block)
            block.container = self

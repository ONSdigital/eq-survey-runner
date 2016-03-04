class Group(object):

    def __init__(self):
        self.id = None
        self.title = None
        self.blocks = []

    def add_block(self, block):
        if block not in self.blocks:
            self.blocks.append(block)

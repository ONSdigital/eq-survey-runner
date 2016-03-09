class Group(object):

    def __init__(self):
        self.id = None
        self.title = None
        self.blocks = []
        self.container = None

    def add_block(self, block):
        if block not in self.blocks:
            self.blocks.append(block)
            block.container = self

    def get_item_by_id(self, id):
        if id == self.id:
            return self
        else:
            item = None
            for block in self.blocks:
                candidate = block.get_item_by_id(id)
                if candidate is not None:
                    item = candidate
            return item

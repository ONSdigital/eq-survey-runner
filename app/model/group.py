class Group(object):

    def __init__(self):
        self.id = None
        self.title = None
        self.blocks = []
<<<<<<< 6d7cf85406a795cde7d9e0ff8c91cb502087d2c1
=======
        self.container = None
>>>>>>> eq-1 validation basics

    def add_block(self, block):
        if block not in self.blocks:
            self.blocks.append(block)
<<<<<<< 6d7cf85406a795cde7d9e0ff8c91cb502087d2c1
=======
            block.container = self
>>>>>>> eq-1 validation basics

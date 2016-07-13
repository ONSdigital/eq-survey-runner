

class Block(object):

    def __init__(self, id):
        self.id = id
        self.sections = []
        self.children = self.sections

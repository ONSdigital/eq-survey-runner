

class Section(object):
    def __init__(self, id):
        self.id = id
        self.questions = []
        self.children = self.questions

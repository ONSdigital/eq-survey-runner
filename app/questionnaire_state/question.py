

class Question(object):
    def __init__(self, id):
        self.id = id
        self.answers = []
        self.children = self.answers

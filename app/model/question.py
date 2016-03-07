class Question(object):
    def __init__(self):
        self.id = None
        self.title = None
        self.description = None
        self.responses = []

    def add_response(self, response):
        if response not in self.responses:
            self.responses.append(response)

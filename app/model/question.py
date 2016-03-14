class Question(object):
    def __init__(self):
        self.id = None
        self.title = None
        self.description = None
        self.responses = []
        self.container = None
        self.questionnaire = None
        self.validation = None

    def add_response(self, response):
        if response not in self.responses:
            self.responses.append(response)
            response.container = self
            if self.questionnaire:
                self.questionnaire.register_item(response.id, response)

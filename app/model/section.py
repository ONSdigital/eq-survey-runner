class Section(object):
    def __init__(self):
        self.id = None
        self.title = None
        self.questions = []
        self.children = self.questions
        self.container = None
        self.questionnaire = None
        self.validation = None
        self.questionnaire = None
        self.templatable_properties = []

    def add_question(self, question):
        if question not in self.questions:
            self.questions.append(question)
            question.container = self

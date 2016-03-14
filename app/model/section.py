class Section(object):
    def __init__(self):
        self.id = None
        self.title = None
        self.questions = []
        self.container = None
        self.questionnaire = None
        self.validation = None

    def add_question(self, question):
        if question not in self.questions:
            self.questions.append(question)
            question.container = self

    def get_item_by_id(self, id):
        if id == self.id:
            return self
        else:
            for question in self.questions:
                candidate = question.get_item_by_id(id)
                if candidate is not None:
                    return candidate
            return None

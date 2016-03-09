class Questionnaire(object):
    def __init__(self):
        self.id = None
        self.title = None
        self.survey_id = None
        self.description = None
        self.groups = []

    def add_group(self, group):
        if group not in self.groups:
            self.groups.append(group)
            group.questionnaire = self

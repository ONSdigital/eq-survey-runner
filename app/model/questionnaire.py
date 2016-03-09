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
            group.container = self

    def get_item_by_id(self, id):
        if id == self.id:
            return self
        else:
            item = None
            for group in self.groups:
                candidate = group.get_item_by_id(id)
                if candidate is not None:
                    item = candidate
            return item

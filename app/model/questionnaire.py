class QuestionnaireException(Exception):
    pass


class Questionnaire(object):
    def __init__(self):
        self.id = None
        self.title = None
        self.survey_id = None
        self.description = None
        self.groups = []
        self.item_register = {}

    def add_group(self, group):
        if group not in self.groups:
            self.groups.append(group)
            group.container = self
            self.register_item(group.id, group)

    def register_item(self, item_id, item):

        if item_id in self.item_register.keys():
            raise QuestionnaireException('Duplicate id found - ' + item_id)

        self.item_register[item_id] = item
        item.questionnaire = self

    def get_item_by_id(self, item_id):
        if item_id in self.item_register:
            return self.item_register[item_id]
        raise QuestionnaireException('Item not found - ' + item_id)

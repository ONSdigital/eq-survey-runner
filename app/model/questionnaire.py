from app.model.display import Display


class QuestionnaireException(Exception):
    pass


class Questionnaire(object):
    def __init__(self):
        self.id = None
        self.title = None
        self.survey_id = None
        self.description = None
        self.groups = []
        self.children = self.groups
        self.validation = None
        self.items_by_id = {}
        self.introduction = None
        self.display = Display()

    def add_group(self, group):
        if group not in self.groups:
            self.groups.append(group)
            group.container = self

    def get_item_by_id(self, item_id):
        if item_id == self.id:
            return self
        else:
            if item_id in self.items_by_id.keys():
                return self.items_by_id[item_id]
            else:
                raise QuestionnaireException('Unknown id \'{}\''.format(item_id))

    def register(self, item):
        if item.id in self.items_by_id.keys():
            raise QuestionnaireException('{} is a duplicate id'.format(item.id))

        self.items_by_id[item.id] = item

        # Build the two-way relationship
        item.questionnaire = self

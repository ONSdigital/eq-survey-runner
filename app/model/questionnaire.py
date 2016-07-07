from app.model.display import Display
from app.model.answer import Answer


class QuestionnaireException(Exception):
    pass


class Questionnaire(object):
    def __init__(self):
        self.eq_id = None
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
        self.aliases = {}

    def add_group(self, group):
        if group not in self.groups:
            self.groups.append(group)
            group.container = self

    def get_item_by_id(self, item_id):
        if item_id == self.id:
            return self
        elif item_id in self.items_by_id.keys():
            return self.items_by_id[item_id]
        else:
            raise QuestionnaireException('Unknown id \'{}\''.format(item_id))

    def register(self, item):
        if item.id in self.items_by_id.keys():
            raise QuestionnaireException('{} is a duplicate id'.format(item.id))

        self.items_by_id[item.id] = item
        self._register_alias(item)

        # Build the two-way relationship
        item.questionnaire = self

    def _register_alias(self, item):
        # Register the alias if the item has one
        if isinstance(item, Answer) and item.alias is not None:
            if item.alias not in self.aliases.keys():
                self.aliases[item.alias] = item.id
            elif self.aliases[item.alias] != item.id:
                raise QuestionnaireException('{} is not a unique alias'.format(item.alias))

    def unregister(self, id):
        if id in self.items_by_id.keys():
            del self.items_by_id[id]

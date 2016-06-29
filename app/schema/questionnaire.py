from app.schema.display import Display
from app.schema.answer import Answer


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
        self.theme = None

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

<<<<<<< HEAD
=======
    def to_json(self):
        json_dict = {
            "mime_type": "application/json/ons/eq",
            "schema_version": "0.0.1",
            "questionnaire_id": self.id,
            "survey_id": self.survey_id,
            "eq_id": self.eq_id,
            "title": self.title,
            "description": self.description,
            "theme": self.theme,
            "groups": [],
            "display": {}
        }

        if self.introduction is not None:
            json_dict['introduction'] = {}
            if self.introduction.legal:
                json_dict['introduction']['legal'] = self.introduction.legal
            if self.introduction.description:
                json_dict['introduction']['description'] = self.introduction.description

        for group in self.groups:
            json_dict['groups'].append(group.to_json())

        if self.validation is not None:
            for validation in self.validation:
                json_dict['validation'].append(validation.to_json())

        if self.display is not None:
            json_dict['display'] = self.display.to_json()

        return json_dict

    def __eq__(self, other):
        if id(self) == id(other):
            return True

        if isinstance(other, Questionnaire):
            properties_match = self.id == other.id and \
                self.title == other.title and \
                self.description == other.description and \
                self.survey_id == other.survey_id and \
                self.eq_id == self.eq_id

            groups_match = True
            if len(self.groups) != len(other.groups):
                return False

            for index, group in enumerate(self.groups):
                if group != other.groups[index]:
                    return False

            validations_match = True
            if self.validation is not None and other.validation is not None:
                if len(self.validation) != len(other.validation):
                    return False

                for index, validation in enumerate(self.validation):
                    if validation != other.validation[index]:
                        return False

            return properties_match and groups_match and validations_match

        else:
            return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.id, self.eq_id, self.title, self.description, self.survey_id, self.groups, self.validation))

    def unregister(self, id):
        if id in self.items_by_id.keys():
            del self.items_by_id[id]

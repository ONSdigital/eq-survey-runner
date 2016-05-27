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

    def to_json(self):
        json_dict = {
            "mime_type": "application/json/ons/eq",
            "schema_version": "0.0.1",
            "questionnaire_id": "23",
            "survey_id": self.survey_id,
            "title": self.title,
            "description": self.description,
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
        if isinstance(other, Questionnnaire):
            properties_match = self.id == other.id and \
                               self.title == other.title

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
            else:
                return False

            return properties_match and groups_match and validations_match

        else:
            return False

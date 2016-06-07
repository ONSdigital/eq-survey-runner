from app.model.display import Display


class Block(object):
    def __init__(self):
        self.id = None
        self.title = None
        self.sections = []
        self.children = self.sections
        self.container = None
        self.questionnaire = None
        self.validation = None
        self.questionnaire = None
        self.templatable_properties = []
        self.display = Display()

    def add_section(self, section):
        if section not in self.sections:
            self.sections.append(section)
            section.container = self

    def to_json(self):
        json_dict = {
            "id": self.id,
            "title": self.title,
            "sections": [],
            "validation": [],
            "display": {}
        }

        for section in self.sections:
            json_dict['sections'].append(section.to_json())

        if self.validation is not None:
            for validation in self.validation:
                json_dict['validation'].append(validation.to_json())

        if self.display is not None:
            json_dict['display'] = self.display.to_json()

        return json_dict

    def __eq__(self, other):
        if id(self) == id(other):
            return True

        if isinstance(other, Block):
            properties_match = self.id == other.id and \
                               self.title == other.title

            sections_match = True
            if len(self.sections) != len(other.sections):
                return False

            for index, section in enumerate(self.sections):
                if section != other.sections[index]:
                    return False

            validations_match = True
            if self.validation is not None and other.validation is not None:
                if len(self.validation) != len(other.validation):
                    return False

                for index, validation in enumerate(self.validation):
                    if validation != other.validation[index]:
                        return False

            templatable_properties_match = False
            if len(self.templatable_properties) != len(other.templatable_properties):
                return False

            for index, templatable_property in enumerate(self.templatable_properties):
                if templatable_property not in other.templatable_properties:
                    return False

            return properties_match and sections_match and validations_match and templatable_properties_match

        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

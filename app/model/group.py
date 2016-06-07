from app.model.display import Display


class Group(object):

    def __init__(self):
        self.id = None
        self.title = None
        self.blocks = []
        self.children = self.blocks
        self.container = None
        self.questionnaire = None
        self.validation = None
        self.questionnaire = None
        self.templatable_properties = []
        self.display = Display()

    def add_block(self, block):
        if block not in self.blocks:
            self.blocks.append(block)
            block.container = self

    def to_json(self):
        json_dict = {
            "id": self.id,
            "title": self.title,
            "blocks": [],
            "validation": [],
            "display": {}
        }

        for block in self.blocks:
            json_dict['blocks'].append(block.to_json())

        if self.validation is not None:
            for validation in self.validation:
                json_dict['validation'].append(validation.to_json())

        if self.display is not None:
            json_dict['display'] = self.display.to_json()

        return json_dict

    def __eq__(self, other):
        if id(self) == id(other):
            return True

        if isinstance(other, Group):
            properties_match = self.id == other.id and \
                               self.title == other.title

            blocks_match = True
            if len(self.blocks) != len(other.blocks):
                return False

            for index, block in enumerate(self.blocks):
                if block != other.blocks[index]:
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

            return properties_match and blocks_match and validations_match and templatable_properties_match

        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

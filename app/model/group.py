from app.model.display import Display
from app.libs.utils import eq_helper_lists_equivalent


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

            blocks_match = eq_helper_lists_equivalent(self.blocks, other.blocks)
            validations_match = eq_helper_lists_equivalent(self.validation, other.validation)
            templatable_properties_match = eq_helper_lists_equivalent(self.templatable_properties, other.templatable_properties)

            return properties_match and blocks_match and validations_match and templatable_properties_match

        else:
            return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.id, self.title))

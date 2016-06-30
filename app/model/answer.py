from app.libs.utils import eq_helper_lists_equivalent
from app.libs.utils import eq_helper_dicts_equivalent


class Answer(object):
    def __init__(self):
        self.id = None
        self.label = ""
        self.guidance = ""
        self.type = None
        self.code = None
        self.container = None
        self.mandatory = False
        self.validation = None
        self.questionnaire = None
        self.display = None
        self.messages = {}
        self.templatable_properties = []
        self.options = []

    def to_json(self):
        json_dict = {
            "id": self.id,
            "label": self.label,
            "guidance": self.guidance,
            "type": self.type,
            "q_code": self.code,
            "validation": {
                "messages": {}
            },
            "mandatory": self.mandatory,
            'display': {},
            'options': []
        }

        for key, value in self.messages.items():
            json_dict['validation']['messages'][key] = value

        if self.display is not None:
            json_dict['display'] = {"properties": self.display.properties}

        for option in self.options:
            json_dict['options'].append(option)

        return json_dict

    def __eq__(self, other):
        if id(self) == id(other):
            return True

        if isinstance(other, Answer):
            properties_match = self.id == other.id and \
                               self.label == other.label and \
                               self.guidance == other.guidance and \
                               self.type == other.type and \
                               self.code == other.code and \
                               self.mandatory == other.mandatory

            validations_match = eq_helper_lists_equivalent(self.validation, other.validation)
            templatable_properties_match = eq_helper_lists_equivalent(self.templatable_properties, other.templatable_properties)
            messages_match = eq_helper_dicts_equivalent(self.messages, other.messages)

            return properties_match and validations_match and templatable_properties_match and messages_match

        else:
            return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.id, self.label, self.guidance, self.type, self.code, self.mandatory))  # NOQA

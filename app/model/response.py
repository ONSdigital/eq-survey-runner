class Response(object):
    def __init__(self):
        self.id = None
        self.label = None
        self.guidance = None
        self.type = None
        self.code = None
        self.container = None
        self.mandatory = None
        self.validation = None
        self.questionnaire = None
        self.display = None
        self.messages = {}
        self.templatable_properties = []

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
            'display': {}
        }

        for key, value in self.messages.items():
            json_dict['validation']['messages'][key] = value

        if self.display is not None:
            json_dict['display'] = self.display.to_json()

        return json_dict

    def __eq__(self, other):
        if id(self) == id(other):
            return True

        if isinstance(other, Response):
            properties_match = self.id == other.id and \
                               self.label == other.label and \
                               self.guidance == other.guidance and \
                               self.type == other.type and \
                               self.code == other.code and \
                               self.mandatory == other.mandatory

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

            messages_match = True
            if len(self.messages) != len(other.messages):
                return False

            for index, message in self.messages.items():
                if message not in other.messages:
                    return False

            return properties_match and validations_match and templatable_properties_match and messages_match

        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

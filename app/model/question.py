from app.model.display import Display


class Question(object):
    def __init__(self):
        self.id = None
        self.title = None
        self.description = None
        self.responses = []
        self.children = self.responses
        self.container = None
        self.questionnaire = None
        self.validation = None
        self.questionnaire = None
        self.templatable_properties = ['description']
        self.display = Display()
        self.type = None

    def add_response(self, response):
        if response not in self.responses:
            self.responses.append(response)
            response.container = self

    def to_json(self):
        json_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "responses": [],
            "validation": [],
            "display": {},
            "type": self.type
        }

        for response in self.responses:
            json_dict['responses'].append(response.to_json())

        if self.validation is not None:
            for validation in self.validation:
                json_dict['validation'].append(validation.to_json())

        if self.display is not None:
            json_dict['display'] = self.display.to_json()

        return json_dict

    def __eq__(self, other):
        if id(self) == id(other):
            return True

        if isinstance(other, Question):
            properties_match = self.id == other.id and \
                               self.title == other.title and \
                               self.description == other.description and \
                               self.type == other.type

            responses_match = True
            if len(self.responses) != len(other.responses):
                return False

            for index, response in enumerate(self.responses):
                if response != other.responses[index]:
                    return False

            validations_match = True
            if self.validation is not None and other.validation is not None:
                if len(self.validation) != len(other.validation):
                    return False

                for index, validation in enumerate(self.validation):
                    if validation != other.validation[index]:
                        return False

            templatable_properties_match = True
            if len(self.templatable_properties) != len(other.templatable_properties):
                return False

            for index, templatable_property in enumerate(self.templatable_properties):
                if templatable_property not in other.templatable_properties:
                    return False

            return properties_match and responses_match and validations_match and templatable_properties_match

        else:
            return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.id, self.title, self.description, self.type))

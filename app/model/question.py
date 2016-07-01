from app.model.display import Display
from app.libs.utils import eq_helper_lists_equivalent


class Question(object):
    def __init__(self):
        self.id = None
        self.title = None
        self.description = ""
        self.answers = []
        self.children = self.answers
        self.container = None
        self.questionnaire = None
        self.validation = None
        self.questionnaire = None
        self.templatable_properties = ['title', 'description']
        self.display = Display()
        self.type = None

    def add_answer(self, answer):
        if answer not in self.answers:
            self.answers.append(answer)
            answer.container = self

    def to_json(self):
        json_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "answers": [],
            "validation": [],
            "display": {},
            "type": self.type
        }

        for answer in self.answers:
            json_dict['answers'].append(answer.to_json())

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

            answers_match = eq_helper_lists_equivalent(self.answers, other.answers)
            validations_match = eq_helper_lists_equivalent(self.validation, other.validation)
            templatable_properties_match = eq_helper_lists_equivalent(self.templatable_properties, other.templatable_properties)

            return properties_match and answers_match and validations_match and templatable_properties_match

        else:
            return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.id, self.title, self.description, self.type))

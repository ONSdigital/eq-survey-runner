from app.questionnaire_state.answer import Answer as State
from app.schema.item import Item


class Answer(Item):
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
        self.alias = None

    def construct_state(self):
        return State(self.id)

    def get_state_class(self):
        return State

    @staticmethod
    def get_instance(answer_type):
        # Do the imports here to avoid circular dependencies
        # TODO: Refactor out into a factory of some sort
        from app.schema.questionnaire import QuestionnaireException

        from app.schema.answers.checkbox_answer import CheckboxAnswer
        from app.schema.answers.currency_answer import CurrencyAnswer
        from app.schema.answers.date_answer import DateAnswer
        from app.schema.answers.integer_answer import IntegerAnswer
        from app.schema.answers.percentage_answer import PercentageAnswer
        from app.schema.answers.positiveinteger_answer import PositiveIntegerAnswer
        from app.schema.answers.radio_answer import RadioAnswer
        from app.schema.answers.textarea_answer import TextareaAnswer
        from app.schema.answers.textfield_answer import TextfieldAnswer

        answer_type = answer_type.upper()

        if answer_type == 'CHECKBOX':
            return CheckboxAnswer()
        elif answer_type == 'CURRENCY':
            return CurrencyAnswer()
        elif answer_type == 'DATE':
            return DateAnswer()
        elif answer_type == 'INTEGER':
            return IntegerAnswer()
        elif answer_type == 'PERCENTAGE':
            return PercentageAnswer()
        elif answer_type == 'POSITIVEINTEGER':
            return PositiveIntegerAnswer()
        elif answer_type == 'RADIO':
            return RadioAnswer()
        elif answer_type == 'TEXTAREA':
            return TextareaAnswer()
        elif answer_type == 'TEXTFIELD':
            return TextfieldAnswer()
        else:
            raise QuestionnaireException('Unknown answer type "{}"'.format(answer_type))

    def get_typed_value(self, post_vars):
        pass

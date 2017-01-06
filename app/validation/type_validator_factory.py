from app.schema.answer import Answer
from app.schema.question import Question
from app.validation.date_range_check import DateRangeCheck
from app.validation.date_type_check import DateTypeCheck
from app.validation.integer_type_check import IntegerTypeCheck
from app.validation.percentage_type_check import PercentageTypeCheck
from app.validation.positive_integer_type_check import PositiveIntegerTypeCheck
from app.validation.textarea_type_check import TextAreaTypeCheck


class TypeValidatorFactoryException(Exception):
    pass


class TypeValidatorFactory(object):

    @staticmethod
    def get_validators_by_type(item):
        """get_validators_by_type

        Given a type, returns a list of validator instances used for basic
        type checking
        """
        answer_validators = {
            'INTEGER': [IntegerTypeCheck],
            'POSITIVEINTEGER': [PositiveIntegerTypeCheck],
            'CURRENCY': [PositiveIntegerTypeCheck],
            'PERCENTAGE': [PercentageTypeCheck],
            'DATE': [DateTypeCheck],
            'TEXTAREA': [TextAreaTypeCheck],
            'RADIO': [],
            'CHECKBOX': [],
            'TEXTFIELD': [],
            }

        question_validators = {
            'DATERANGE': [DateRangeCheck],
            'INTEGER': [],
            'POSITIVEINTEGER': [],
            'CURRENCY': [],
            'DATE': [],
            'TEXTAREA': [],
            'RADIOS': [],
            'CHECKBOXS': [],
            'CHECKBOXES': [],
            'GENERAL': [],
        }

        i_type = item.type.upper()

        validators = []
        if isinstance(item, Answer):
            try:
                for validator in answer_validators[i_type]:
                    validators.append(validator())
            except KeyError:
                err_msg = '\'{}\' is not a known answer type'.format(i_type)
                raise TypeValidatorFactoryException(err_msg)

        elif isinstance(item, Question):
            try:
                for validator in question_validators[i_type]:
                    validators.append(validator())
            except KeyError:
                err_msg = '\'{}\' is not a known question type'.format(i_type)
                raise TypeValidatorFactoryException(err_msg)
        return validators

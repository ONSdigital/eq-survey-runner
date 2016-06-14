from app.validation.integer_type_check import IntegerTypeCheck
from app.validation.positive_integer_type_check import PositiveIntegerTypeCheck
from app.validation.date_type_check import DateTypeCheck
from app.validation.textarea_type_check import TextAreaTypeCheck
from app.validation.date_range_check import DateRangeCheck
from app.model.response import Response
from app.model.question import Question


class TypeValidatorFactoryException(Exception):
    pass


class TypeValidatorFactory(object):

    @staticmethod
    def get_validators_by_type(item):
        """get_validators_by_type

        Given a type, returns a list of validator instances used for basic
        type checking
        """
        response_validators = {
            'INTEGER': [IntegerTypeCheck],
            'POSITIVEINTEGER': [PositiveIntegerTypeCheck],
            'CURRENCY': [PositiveIntegerTypeCheck],
            'DATE': [DateTypeCheck],
            'TEXTAREA': [TextAreaTypeCheck],
            'RADIO': [],
            'CHECKBOX': []
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
            'CHECKBOXES': []
        }

        i_type = item.type.upper()

        validators = []
        if isinstance(item, Response):
            try:
                for validator in response_validators[i_type]:
                    validators.append(validator())
            except KeyError:
                err_msg = '\'{}\' is not a known response type'.format(i_type)
                raise TypeValidatorFactoryException(err_msg)

        elif isinstance(item, Question):
            try:
                for validator in question_validators[i_type]:
                    validators.append(validator())
            except KeyError:
                err_msg = '\'{}\' is not a known question type'.format(i_type)
                raise TypeValidatorFactoryException(err_msg)
        return validators

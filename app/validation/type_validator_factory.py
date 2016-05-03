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

        validators = []
        if isinstance(item, Response):
            if item.type.upper() == 'INTEGER':
                validators.append(IntegerTypeCheck())
            elif item.type.upper() == "POSTIVEINTEGER":
                validators.append(PositiveIntegerTypeCheck())
            elif item.type.upper() == 'CURRENCY':
                validators.append(PositiveIntegerTypeCheck())
            elif item.type.upper() == 'DATE':
                validators.append(DateTypeCheck())
            elif item.type.upper() == 'TEXTAREA':
                validators.append(TextAreaTypeCheck())
            else:
                raise TypeValidatorFactoryException('\'{}\' is not a known response type'.format(item.type))

        elif isinstance(item, Question):
            if item.type.upper() == 'DATERANGE':
                validators.append(DateRangeCheck())
        return validators

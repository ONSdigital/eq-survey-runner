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
        i_type = item.type

        validators = []
        if isinstance(item, Response):
            if i_type.upper() == 'INTEGER':
                validators.append(IntegerTypeCheck())
            elif i_type.upper() == "POSTIVEINTEGER":
                validators.append(PositiveIntegerTypeCheck())
            elif i_type.upper() == 'CURRENCY':
                validators.append(PositiveIntegerTypeCheck())
            elif i_type.upper() == 'DATE':
                validators.append(DateTypeCheck())
            elif i_type.upper() == 'TEXTAREA':
                validators.append(TextAreaTypeCheck())
            else:
                raise TypeValidatorFactoryException('\'{}\' is not a known response type'.format(i_type))

        elif isinstance(item, Question):
            if i_type.upper() == 'DATERANGE':
                validators.append(DateRangeCheck())
        return validators

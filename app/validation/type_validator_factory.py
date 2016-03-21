from app.validation.integer_type_check import IntegerTypeCheck
from app.validation.positive_integer_type_check import PositiveIntegerTypeCheck
from app.validation.date_type_check import DateTypeCheck
from app.validation.textarea_type_check import TextAreaTypeCheck


class TypeValidatorFactoryException(Exception):
    pass


class TypeValidatorFactory(object):

    @staticmethod
    def get_validators_by_type(response_type):
        """get_validators_by_type

        Given a type, returns a list of validator instances used for basic
        type checking
        """
        validators = []

        if response_type.upper() == 'INTEGER':
            validators.append(IntegerTypeCheck())
        elif response_type.upper() == "POSTIVEINTEGER":
            validators.append(PositiveIntegerTypeCheck())
        elif response_type.upper() == 'CURRENCY':
            validators.append(PositiveIntegerTypeCheck())
        elif response_type.upper() == 'DATERANGE':
            validators.append(DateTypeCheck())
        elif response_type.upper() == 'TEXTAREA':
            validators.append(TextAreaTypeCheck())
        else:
            raise TypeValidatorFactoryException('\'{}\' is not a known response type'.format(response_type))

        return validators

from app.validation.integer_type_check import IntegerTypeCheck


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
        elif response_type.upper() == 'CURRENCY':
            validators.append(IntegerTypeCheck())
        else:
            raise TypeValidatorFactoryException('\'{}\' is not a known response type'.format(response_type))

        return validators

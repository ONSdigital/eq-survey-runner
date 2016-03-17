from app.validation.abstract_validator import AbstractValidator
from app.validation.validation_result import ValidationResult


class PositiveIntegerTypeCheck(AbstractValidator):

    """
    Validate that the users answer is an integer
    :param user_answer: The answer the user provided for the response
    :return: ValidationResult(): An object containing the result of the validation
    """

    def validate(self, user_answer):
        result = ValidationResult(False)
        try:
            integer_value = int(user_answer)        # NOQA
            if integer_value < 0:
                result.errors.append("'{value}' is less than zero".format(value=user_answer))
                return result
            result.is_valid = True
        except:
            result.is_valid = False
            result.errors.append("'{value}' is not a whole number".format(value=user_answer))

        return result

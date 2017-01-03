from app.validation.abstract_validator import AbstractValidator
from app.validation.validation_result import ValidationResult


class PositiveIntegerTypeCheck(AbstractValidator):

    def __init__(self, minimum=0, maximum=9999999999):
        self.min = minimum
        self.max = maximum

    def validate(self, user_answer):
        """
        Validate that the users answer is an integer
        :param user_answer: The answer the user provided for the response
        :return: ValidationResult(): An object containing the result of the validation
        """
        result = ValidationResult(False)
        try:
            integer_value = int(user_answer)        # NOQA
            if integer_value < self.min:
                result.errors.append(AbstractValidator.NEGATIVE_INTEGER)
                return result
            if integer_value > self.max:          # 10 digits
                result.errors.append(AbstractValidator.INTEGER_TOO_LARGE)
                return result

            result.is_valid = True
        except (ValueError, TypeError):
            result.is_valid = False
            result.errors.append(AbstractValidator.NOT_INTEGER)

        return result

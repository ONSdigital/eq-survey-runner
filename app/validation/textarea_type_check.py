from app.validation.abstract_validator import AbstractValidator
from app.validation.validation_result import ValidationResult


# TODO we need to think about types as TextArea is tied too much to HTML
class TextAreaTypeCheck(AbstractValidator):

    def validate(self, user_answer):
        """
        Validate that the users answer is a string and only contains alphanumeric characters
        :param user_answer: The answer the user provided for the response
        :return: ValidationResult(): An object containing the result of the validation
        """
        result = ValidationResult(False)
        if isinstance(user_answer, str):
            result.is_valid = not user_answer.isspace()
        else:
            result.is_valid = False
            result.errors.append(AbstractValidator.NOT_STRING)
        return result

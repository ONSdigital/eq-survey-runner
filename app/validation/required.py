from app.validation.i_validator import IValidator
from app.validation.validation_result import ValidationResult


class Required(IValidator):

    """
    Validate that a field is required
    :param user_answer: The answer the user provided for the response
    :return: ValidationResult(): An object containing the result of the validation
    """

    def validate(self, user_answer):

        validation_result = ValidationResult()

        if user_answer and not str(user_answer).isspace():
            validation_result.update_state(True)
        else:
            validation_result.update_state(False)
            validation_result.errors.append("This field is required")
        return validation_result

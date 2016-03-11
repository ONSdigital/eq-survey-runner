from app.validation.i_validator import IValidator
from app.validation.validation_result import ValidationResult


class Integer(IValidator):

    """
    Validate that the users answer is an integer
    :param user_answer: The answer the user provided for the response
    :return: ValidationResult(): An object containing the result of the validation
    """

    def validate(self, user_answer):

        validation_result = ValidationResult()

        if isinstance(user_answer, int):
            validation_result.update_state(True)
        else:
            validation_result.update_state(False)
            validation_result.errors.append("This field should be a number")

        return validation_result

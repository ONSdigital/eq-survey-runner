from app.validation.abstract_validator import AbstractValidator
from app.validation.validation_result import ValidationResult


class MandatoryCheck(AbstractValidator):

    """
    Validate that a field is mandatory
    :param user_answer: The answer the user provided for the response
    :return: ValidationResult(): An object containing the result of the validation
    """

    def validate(self, user_answer):
        validation_result = ValidationResult()
        validation_result.is_valid = False

        if isinstance(user_answer, list):
            self._validate_list(user_answer, validation_result)
        else:
            self._validate_single(user_answer, validation_result)

        # We only want ONE error message
        if not validation_result.is_valid:
            validation_result.errors.append(AbstractValidator.MANDATORY)

        return validation_result

    def _validate_list(self, user_answers, validation_result):
        for answer in user_answers:
            self._validate_single(answer, validation_result)
            if validation_result.is_valid:
                # We've found a valid entry in the list, bail out
                return

    def _validate_single(self, user_answer, validation_result):
        if user_answer and not str(user_answer).isspace():
            validation_result.is_valid = True
        else:
            validation_result.is_valid = False

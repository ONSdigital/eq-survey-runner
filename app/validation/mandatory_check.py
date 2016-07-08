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

        if isinstance(user_answer, list):
            for answer in user_answer:
                if answer and not str(answer).isspace():
                    validation_result.is_valid = True
                    return validation_result
                else:
                    validation_result.is_valid = False
                    # We do not return at this point as there may still be
                    # a valid response in the list

            # No valid values in list
            validation_result.errors.append(AbstractValidator.MANDATORY)
        else:
            if user_answer and not str(user_answer).isspace():
                validation_result.is_valid = True
            else:
                validation_result.is_valid = False
                validation_result.errors.append(AbstractValidator.MANDATORY)

        return validation_result

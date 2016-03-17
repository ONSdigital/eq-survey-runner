from app.validation.abstract_validator import AbstractValidator
from app.validation.validation_result import ValidationResult
import time
from flask.ext.babel import gettext


class DateTypeCheck(AbstractValidator):

    """
    Validate that the users answer is a valid date
    :param user_answer: The answer the user provided for the response
    :return: ValidationResult(): An object containing the result of the validation
    """

    def validate(self, user_answer):
        result = ValidationResult(False)
        try:
            date = time.strptime(user_answer, "%d/%m/%Y")  # NOQA
            return ValidationResult(True)
        except ValueError:
            result.errors.append(gettext('This is not a valid date'))
        except TypeError:
            result.errors.append(gettext('This is not a valid date'))
        return result

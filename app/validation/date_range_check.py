import logging

from datetime import datetime

from app.validation.abstract_validator import AbstractValidator
from app.validation.validation_result import ValidationResult


logger = logging.getLogger(__name__)


class DateRangeCheck(AbstractValidator):

    def validate(self, user_answers):
        """
        Validate that the users answer is a valid date range
        :param user_answers: The answer the user provided for the response
        :return: ValidationResult(): An object containing the result of the validation
        """

        result = ValidationResult(False)
        logger.debug('Type Checking question date range with data %s', user_answers)

        try:

            if len(user_answers) == 2:
                from_date = datetime.strptime(user_answers[0], "%d/%m/%Y")
                to_date = datetime.strptime(user_answers[1], "%d/%m/%Y")
                date_diff = to_date - from_date

                if date_diff.total_seconds() > 0:
                    return ValidationResult(True)
                elif date_diff.total_seconds() == 0:
                    result.errors.append(AbstractValidator.INVALID_DATE_RANGE_TO_FROM_SAME)
                    return result
                else:
                    result.errors.append(AbstractValidator.INVALID_DATE_RANGE_TO_BEFORE_FROM)
                    return result

        except ValueError:
            result.errors.append(AbstractValidator.INVALID_DATE)
        except TypeError:
            result.errors.append(AbstractValidator.INVALID_DATE)
        except AttributeError:
            result.errors.append(AbstractValidator.INVALID_DATE)
        return result

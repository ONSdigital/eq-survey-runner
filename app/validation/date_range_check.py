from app.validation.abstract_validator import AbstractValidator
from app.validation.validation_result import ValidationResult
from datetime import datetime

DATE_FROM = "From"
DATE_TO = "To"


class DateRangeCheck(AbstractValidator):

    """
    Validate that the users answer is a valid date range
    :param user_answers: The answer the user provided for the response
    :return: ValidationResult(): An object containing the result of the validation
    """

    def validate(self, user_answers):

        result = ValidationResult(False)
        from_date = None
        to_date = None

        try:

            if DATE_FROM in user_answers.keys():
                from_date = datetime.strptime(user_answers[DATE_FROM], "%d/%m/%Y")
            if DATE_TO in user_answers.keys():
                to_date = datetime.strptime(user_answers[DATE_TO], "%d/%m/%Y")

            if from_date and to_date:
                date_diff = to_date - from_date

                if date_diff.total_seconds() > 0:
                    return ValidationResult(True)
                elif date_diff.total_seconds() == 0:
                    result.errors.append(AbstractValidator.INVALID_DATE_RANGE_SAME)
                    return result
                else:
                    result.errors.append(AbstractValidator.INVALID_DATE_RANGE_DIFF)
                    return result

        except ValueError:
            result.errors.append(AbstractValidator.INVALID_DATE)
        except TypeError:
            result.errors.append(AbstractValidator.INVALID_DATE)
        return result

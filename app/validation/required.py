from i_validator import IValidator
from validation_result import ValidationResult


class Required(IValidator):

    def validate(self, repsone):
        return ValidationResult()

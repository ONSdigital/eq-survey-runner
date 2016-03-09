from app.validation.i_validator import IValidator
from app.validation.validation_result import ValidationResult


class Required(IValidator):

    def validate(self, repsone):
        return ValidationResult()

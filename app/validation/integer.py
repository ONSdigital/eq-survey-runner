from app.validation.i_validator import IValidator
from app.validation.validation_result import ValidationResult


class Integer(IValidator):

    def validate(self, answer):
        result = ValidationResult()
        result.update_state(isinstance(answer, int))
        return result

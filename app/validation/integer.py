from i_validator import IValidator
from validation_result import ValidationResult


class Integer(IValidator):

    def validate(self, answer):
        result = ValidationResult()
        result.update_state(isinstance(answer, int))
        return result


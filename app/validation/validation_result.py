class ValidationResult(object):
    def __init__(self, is_valid=False):
        self.is_valid = is_valid
        self.errors = []
        self.warnings = []

    def is_valid(self):
        return self.is_valid

    def get_errors(self):
        return self.errors

    def get_warnings(self):
        return self.warnings

    def to_dict(self):
        return {
            "valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings,
        }

    def from_dict(self, values):
        self.is_valid = values['valid'] or False
        self.errors = values['errors'] or []
        self.warnings = values['warnings'] or []

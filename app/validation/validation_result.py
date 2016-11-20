class ValidationResult(object):
    def __init__(self, is_valid=False):
        self.is_valid = is_valid
        self.errors = []
        self.warnings = []

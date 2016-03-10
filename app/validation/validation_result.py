class ValidationResult(object):
    def __init__(self, is_valid=False):
        self.is_valid = is_valid

    def is_valid(self):
        return self.is_valid

    def get_errors(self):
        return {}

    def get_warnings(self):
        return {}

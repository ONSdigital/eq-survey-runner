class ValidationResult(object):
    def is_valid(self):
        raise NotImplementedError()

    def get_errors(self):
        raise NotImplementedError()

    def get_warnings(self):
        raise NotImplementedError()

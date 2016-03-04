
class ValidationRule(object):
    def set_context(self, context):
        raise NotImplementedError()

    def can_run(self):
        raise NotImplementedError()

    def validate(self):
        raise NotImplementedError()

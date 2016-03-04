class Validator(object):
    def set_context(self, context):
        raise NotImplementedError()

    def validate(self):
        raise NotImplementedError()

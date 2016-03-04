
class ValidationStore(object):
    # keys are in the format...
    # group:block:section:question:response:<repetition>
    def store_result(self, key, value):
        raise NotImplementedError()

    def get_result(self, key):
        raise NotImplementedError()

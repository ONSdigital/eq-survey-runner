from integer import Integer
from required import Required


class ResponseFactory(object):

    @staticmethod
    def determine_response_class(type):

        if type == "Integer":
            response_class = Integer()
        else:
            response_class = Required()

        return response_class

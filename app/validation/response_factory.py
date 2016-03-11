from app.validation.integer import Integer
from app.validation.required import Required


class ResponseFactoryException(Exception):
    pass

    """
    Determine the class needed to validate
    :validator: The reference name in the model
    :return: response_class: The class to use to validate
    """

class ResponseFactory(object):

    @staticmethod
    def determine_response_class(validator):

        if validator == "Integer":
            response_class = Integer()
        elif validator == "Required":
            response_class = Required()
        else:
            raise ResponseFactoryException('Validator not implemented - ' + validator)

        return response_class

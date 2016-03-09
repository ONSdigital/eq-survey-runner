from app.validation.response_factory import ResponseFactory


class ResponseValidator(object):

    @staticmethod
    def validate(response, user_response):
        response_factory = ResponseFactory()
        response_class = response_factory.determine_response_class(response)
        return response_class.validate(user_response)

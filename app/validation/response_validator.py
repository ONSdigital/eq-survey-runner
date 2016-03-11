from app.validation.response_factory import ResponseFactory


class ResponseValidator(object):

    """
    Validate the users answer
    :param validator: The models validator code
    :param user_answer: The answer provided by the user
    :return: ValidationResult(): An object containing the result of the validation
    """
    @staticmethod
    def validate(validator, user_answer):
        response_factory = ResponseFactory()
        response_class = response_factory.determine_response_class(validator)
        return response_class.validate(user_answer)


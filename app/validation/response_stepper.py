from app.validation.response_validator import ResponseValidator
from app.validation.i_validation_steps import IValidationSteps

CONST_REQUIRED = "Required"

class ResponseStepper(IValidationSteps):

    """
    Step threw each answer, checking they are requried before validating their type,
    :param questionnaire: The questionnaire model
    :param user_answer: The answers provide by the user
    :param validation_store: The location the results are stored in
    """

    def validation_steps(self, questionnaire, user_answers, validation_store):

        for value, key in enumerate(user_answers):
            # map the users answer to the id in the model
            response = questionnaire.get_item_by_id(key)

            if response.required:
                required_result = self.validate_answer(CONST_REQUIRED, user_answers[key])
                validation_store.store_result(key, required_result)

            if required_result.is_valid:
                validation_result = self.validate_answer(response.type, user_answers[key])
                validation_store.store_result(key, validation_result)

    """
    Validate the answer.
    :param validator: The models validator code
    :param user_answer: The answer provided by the user
    :return ValidationResult(): An object containing results of the validation
    """

    @staticmethod
    def validate_answer(validator, user_answer):
        return ResponseValidator().validate(validator, user_answer)

from app.validation.validation_store import ValidationStoreFactory
from app.validation.response_stepper import ResponseStepper


class ValidatorStepper(object):

    def __init__(self):
        self.validation_results = ValidationStoreFactory.create_validation_store()

    """
    Validate the questionnaire at response level
    :param questionnaire:The questionnaire model
    :param user_answers: The answers the user provided for the response
    :return: ValidationStore(): The results of validating the questionnaire
    """

    def validator_stepper(self, questionnaire, user_answers):

        ResponseStepper().validation_steps(questionnaire, user_answers, self.validation_results)
        return self.validation_results

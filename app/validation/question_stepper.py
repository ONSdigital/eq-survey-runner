from i_validation_steps import IValidationSteps
from validation_result import ValidationResult


class QuestionStepper(IValidationSteps):

    '''
      Check the store for each part of the question to see if it can validate
    '''

    def validation_steps(self, section, question, validation_store):

        question_result = ValidationResult()

        for response in question.responses:
            response_result = validation_store.get_result(response.id)
            if response_result == "Not validated" or not response_result.is_valid:
                question_result.update_state(False)
                validation_store.store_result(question.id, question_result)
                return

        question_result.update_state(True)
        validation_store.store_result(question.id, question_result)

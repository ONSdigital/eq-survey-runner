from app.validation.response_validator import ResponseValidator
from app.validation.i_validation_steps import IValidationSteps


class ResponseStepper(IValidationSteps):

    '''
      map user_answers to response (temporary) then store validation result
    '''

    def validation_steps(self, question, user_answers, validation_store):

        for value, key in enumerate(user_answers):
            response = self.map_user_answer_to_response(key, question)
            validation_result = ResponseValidator().validate(response.type, user_answers[key])
            validation_store.store_result(key, validation_result)

    @staticmethod
    def map_user_answer_to_response(user_answer_id, question):

        for response in question.responses:
            if response.id == user_answer_id:
                return response

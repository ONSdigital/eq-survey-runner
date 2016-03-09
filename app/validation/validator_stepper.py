from app.validation.validation_store import ValidationStore
from app.validation.question_stepper import QuestionStepper
from app.validation.response_stepper import ResponseStepper


class ValidatorStepper(object):

    def __init__(self):
        self.validation_results = ValidationStore()

    '''
       Step through each container validating,
       n.b container element e.g. first element, won't exist when
       model is updated, (replaced by get_object on model)
    '''

    def validator_stepper(self, section, user_answers):

        # Place holder, which will be remove, reason above
        question = section.questions[0]

        ResponseStepper().validation_steps(question, user_answers, self.validation_results)
        QuestionStepper().validation_steps(section, question, self.validation_results)

        return self.validation_results

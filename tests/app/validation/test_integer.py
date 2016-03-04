import unittest
from app.validation.validator_stepper import ValidatorStepper
from app.model.response import Response
from app.model.question import Question
from app.model.section import Section

class IntegerTest(unittest.TestCase):

    def test_integer_fail(self):

        section_1 = Section()

        question_1 = Question()
        question_1.id = "0df6fe58-25c9-430f-b157-9dc6b5a7646f"
        section_1.add_question(question_1)

        response_1 = Response()
        response_2 = Response()
        question_1.add_response(response_1)
        question_1.add_response(response_2)

        response_1.type = "Integer"
        response_1.id = "69ed19a4-f2ee-4742-924d-b64b9fa09499"
        response_2.type = "Integer"
        response_2.id = "709c9f96-2757-4cf3-ba48-808c6c616848"
        user_answers ={"69ed19a4-f2ee-4742-924d-b64b9fa09499":1, "709c9f96-2757-4cf3-ba48-808c6c616848":"a"}

        validation_results= ValidatorStepper().validator_stepper(section_1, user_answers)

        self.assertEquals(True, validation_results.get_result("69ed19a4-f2ee-4742-924d-b64b9fa09499").is_valid)
        self.assertEquals(False, validation_results.get_result("709c9f96-2757-4cf3-ba48-808c6c616848").is_valid)
        self.assertEquals(False, validation_results.get_result("0df6fe58-25c9-430f-b157-9dc6b5a7646f").is_valid)

    def test_integer_pass(self):

        section_1 = Section()

        question_1 = Question()
        question_1.id = "0df6fe58-25c9-430f-b157-9dc6b5a7646f"
        section_1.add_question(question_1)

        response_1 = Response()
        response_2 = Response()
        question_1.add_response(response_1)
        question_1.add_response(response_2)

        response_1.type = "Integer"
        response_1.id = "69ed19a4-f2ee-4742-924d-b64b9fa09499"
        response_2.type = "Integer"
        response_2.id = "709c9f96-2757-4cf3-ba48-808c6c616848"
        user_answers ={"69ed19a4-f2ee-4742-924d-b64b9fa09499":1, "709c9f96-2757-4cf3-ba48-808c6c616848": 2}

        validation_results= ValidatorStepper().validator_stepper(section_1, user_answers)

        self.assertEquals(True, validation_results.get_result("69ed19a4-f2ee-4742-924d-b64b9fa09499").is_valid)
        self.assertEquals(True, validation_results.get_result("709c9f96-2757-4cf3-ba48-808c6c616848").is_valid)
        self.assertEquals(True, validation_results.get_result("0df6fe58-25c9-430f-b157-9dc6b5a7646f").is_valid)


if __name__ == '__main__':
    unittest.main()

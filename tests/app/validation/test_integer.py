import unittest
from app.validation.validator_stepper import ValidatorStepper
from app.model.response import Response
from app.model.question import Question
from app.model.section import Section
from app.model.block import Block
from app.model.questionnaire import Questionnaire
from app.model.group import Group


class IntegerTest(unittest.TestCase):

    def test_integer_required_fail(self):

        questionnaire_1 = Questionnaire()
        questionnaire_1.id = "d68421bf-14a6-447d-8ebe-12284b8e4407"
        group_1 = Group()
        group_1.id = "be0296a5-3235-40e5-a7b0-d1d7dff0ba87"
        block_1 = Block()
        block_1.id = "ce8d7204-615e-42dd-9e46-17744ac39b04"
        section_1 = Section()
        section_1.id = "e109368f-46f2-4283-982e-eebf76051eac"
        questionnaire_1.add_group(group_1)
        group_1.add_block(block_1)
        block_1.add_section(section_1)

        question_1 = Question()
        question_1.id = "0df6fe58-25c9-430f-b157-9dc6b5a7646f"
        section_1.add_question(question_1)

        response_1 = Response()
        response_2 = Response()

        response_1.type = "Integer"
        response_1.id = "69ed19a4-f2ee-4742-924d-b64b9fa09499"
        response_2.type = "Integer"
        response_2.id = "709c9f96-2757-4cf3-ba48-808c6c616848"
        user_answers ={"69ed19a4-f2ee-4742-924d-b64b9fa09499":1, "709c9f96-2757-4cf3-ba48-808c6c616848": " "}

        validation_results= ValidatorStepper().validator_stepper(questionnaire_1, user_answers)


        self.assertEquals(True, validation_results.get_result("69ed19a4-f2ee-4742-924d-b64b9fa09499").is_valid)
        self.assertEquals(False, validation_results.get_result("709c9f96-2757-4cf3-ba48-808c6c616848").is_valid)
        self.assertEquals(['This field is required'],
                          validation_results.get_result("709c9f96-2757-4cf3-ba48-808c6c616848").get_errors())

    def test_integer_required_fail(self):

        questionnaire_1 = Questionnaire()
        questionnaire_1.id = "d68421bf-14a6-447d-8ebe-12284b8e4407"
        group_1 = Group()
        group_1.id = "be0296a5-3235-40e5-a7b0-d1d7dff0ba87"
        block_1 = Block()
        block_1.id = "ce8d7204-615e-42dd-9e46-17744ac39b04"
        section_1 = Section()
        section_1.id = "e109368f-46f2-4283-982e-eebf76051eac"
        questionnaire_1.add_group(group_1)
        group_1.add_block(block_1)
        block_1.add_section(section_1)

        question_1 = Question()
        question_1.id = "0df6fe58-25c9-430f-b157-9dc6b5a7646f"
        section_1.add_question(question_1)

        response_1 = Response()
        response_2 = Response()

        response_1.type = "Integer"
        response_1.id = "69ed19a4-f2ee-4742-924d-b64b9fa09499"
        response_2.type = "Integer"
        response_2.id = "709c9f96-2757-4cf3-ba48-808c6c616848"
        question_1.add_response(response_1)
        question_1.add_response(response_2)
        user_answers ={"69ed19a4-f2ee-4742-924d-b64b9fa09499":1, "709c9f96-2757-4cf3-ba48-808c6c616848": "a"}

        validation_results= ValidatorStepper().validator_stepper(questionnaire_1, user_answers)

        self.assertEquals(True, validation_results.get_result("69ed19a4-f2ee-4742-924d-b64b9fa09499").is_valid)
        self.assertEquals(False, validation_results.get_result("709c9f96-2757-4cf3-ba48-808c6c616848").is_valid)
        self.assertEquals(['This field should be a number'],
                          validation_results.get_result("709c9f96-2757-4cf3-ba48-808c6c616848").get_errors())

    def test_integer_pass(self):

        questionnaire_1 = Questionnaire()
        questionnaire_1.id = "d68421bf-14a6-447d-8ebe-12284b8e4407"
        group_1 = Group()
        group_1.id = "be0296a5-3235-40e5-a7b0-d1d7dff0ba87"
        block_1 = Block()
        block_1.id = "ce8d7204-615e-42dd-9e46-17744ac39b04"
        section_1 = Section()
        section_1.id = "e109368f-46f2-4283-982e-eebf76051eac"
        questionnaire_1.add_group(group_1)
        group_1.add_block(block_1)
        block_1.add_section(section_1)

        question_1 = Question()
        question_1.id = "0df6fe58-25c9-430f-b157-9dc6b5a7646f"
        section_1.add_question(question_1)

        response_1 = Response()
        response_2 = Response()

        response_1.type = "Integer"
        response_1.id = "69ed19a4-f2ee-4742-924d-b64b9fa09499"
        response_2.type = "Integer"
        response_2.id = "709c9f96-2757-4cf3-ba48-808c6c616848"

        user_answers ={"69ed19a4-f2ee-4742-924d-b64b9fa09499":1, "709c9f96-2757-4cf3-ba48-808c6c616848": 2}

        validation_results= ValidatorStepper().validator_stepper(questionnaire_1, user_answers)

        self.assertEquals(True, validation_results.get_result("69ed19a4-f2ee-4742-924d-b64b9fa09499").is_valid)
        self.assertEquals(True, validation_results.get_result("709c9f96-2757-4cf3-ba48-808c6c616848").is_valid)


if __name__ == '__main__':
    unittest.main()

import unittest
from app.validation.validator import Validator
from app.answers.answer_store import AbstractAnswerStore
from app.validation.validation_store import AbstractValidationStore
from app.validation.abstract_validator import AbstractValidator
from app.validation.validation_result import ValidationResult

from app.model.questionnaire import Questionnaire
from app.model.group import Group
from app.model.block import Block
from app.model.section import Section
from app.model.question import Question
from app.model.answer import Answer


class ValidatorTest(unittest.TestCase):
    def setUp(self):

        self._answer_store = self._create_mock_answers_store()
        self._validation_store = self._create_mock_validation_store()
        self._schema = self._create_schema()

    def test_validate(self):
        validator = Validator(self._schema, self._validation_store, self._answer_store)

        # Override the factory class used for Type Checking
        validator._type_validator_factory_class = MockTypeValidatorFactory

        answer_1 = self._schema.get_item_by_id("69ed19a4-f2ee-4742-924d-b64b9fa09499")
        answer_1.type = 'succeed'
        answer_1.mandatory = False

        question_1 = self._schema.get_item_by_id("0df6fe58-25c9-430f-b157-9dc6b5a7646f")
        question_1.validation = [RaisingValidator()]    # Raises an exception when called, which we can track

        # Test that when we call validate with our answer it not only validates the answer,
        # but propagates up the tree caliing validate

        with self.assertRaises(Exception) as exc:
            validator.validate({"69ed19a4-f2ee-4742-924d-b64b9fa09499": None})
            self.assertEquals('validate called against \'None\'', exc.message)

    def test_validate_item(self):
        validator = Validator(self._schema, self._validation_store, self._answer_store)

        # Override the factory class used for Type Checking
        validator._type_validator_factory_class = MockTypeValidatorFactory

        """
        Uses the MockTypeValidatorFactory to determine the validation result based
        on the type.  Here we are checking that _validate_item handles the "mandatory"
        check correctly.
        """
        # check validating a non-mandatory answer
        non_mandatory_answer = self._schema.get_item_by_id("69ed19a4-f2ee-4742-924d-b64b9fa09499")
        non_mandatory_answer.type = "succeed"  # overwrite built in type checking
        non_mandatory_answer.mandatory = False

        result = validator._validate_item(non_mandatory_answer, None)
        self.assertTrue(result.is_valid)

        # Check validating a mandatory answer
        mandatory_answer = self._schema.get_item_by_id("709c9f96-2757-4cf3-ba48-808c6c616848")
        non_mandatory_answer.type = "succeed"  # again, should still fail mandatory
        mandatory_answer.mandatory = True

        result = validator._validate_item(mandatory_answer, None)
        self.assertFalse(result.is_valid)

        """
        Use the MockTypeValidatorFactory to determine the validation result based
        on the type.  We are not checking the Factoyr, we are checking that the
        _validate_item method does the right thing.
        """
        # type-checking a non-mandatory answer (using mock factory)
        non_mandatory_answer = self._schema.get_item_by_id("69ed19a4-f2ee-4742-924d-b64b9fa09499")
        non_mandatory_answer.type = "succeed"  # overwrite built in type checking
        non_mandatory_answer.mandatory = False

        result = validator._validate_item(non_mandatory_answer, "Anything")
        self.assertTrue(result.is_valid)

        # type-checking a non-mandatory answer (using mock)
        non_mandatory_answer = self._schema.get_item_by_id("69ed19a4-f2ee-4742-924d-b64b9fa09499")
        non_mandatory_answer.type = "failure"  # overwrite built in type checking
        non_mandatory_answer.mandatory = False

        result = validator._validate_item(non_mandatory_answer, "Anything")
        self.assertFalse(result.is_valid)

    def test_validate_container(self):
        validator = Validator(self._schema, self._validation_store, self._answer_store)

        # Override the factory class used for Type Checking
        validator._type_validator_factory_class = MockTypeValidatorFactory

        answer_1 = self._schema.get_item_by_id("69ed19a4-f2ee-4742-924d-b64b9fa09499")
        question_1 = self._schema.get_item_by_id("0df6fe58-25c9-430f-b157-9dc6b5a7646f")

        question_1.validation = [RaisingValidator()]    # Raises an exception when called, which we can track

        with self.assertRaises(Exception) as exc:
            validator._validate_container(answer_1.container)
            self.assertEquals('validate called against \'None\'', exc.message)

    def _create_schema(self):
        questionnaire_1 = Questionnaire()
        questionnaire_1.id = "d68421bf-14a6-447d-8ebe-12284b8e4407"

        group_1 = Group()
        group_1.id = "be0296a5-3235-40e5-a7b0-d1d7dff0ba87"
        questionnaire_1.add_group(group_1)
        questionnaire_1.register(group_1)

        block_1 = Block()
        block_1.id = "ce8d7204-615e-42dd-9e46-17744ac39b04"
        group_1.add_block(block_1)
        questionnaire_1.register(block_1)

        section_1 = Section()
        section_1.id = "e109368f-46f2-4283-982e-eebf76051eac"
        block_1.add_section(section_1)
        questionnaire_1.register(section_1)

        question_1 = Question()
        question_1.id = "0df6fe58-25c9-430f-b157-9dc6b5a7646f"
        question_1.type = "Integer"
        section_1.add_question(question_1)
        questionnaire_1.register(question_1)

        answer_1 = Answer()
        answer_1.type = "Integer"
        answer_1.id = "69ed19a4-f2ee-4742-924d-b64b9fa09499"
        question_1.add_answer(answer_1)
        questionnaire_1.register(answer_1)

        answer_2 = Answer()
        answer_2.type = "Integer"
        answer_2.id = "709c9f96-2757-4cf3-ba48-808c6c616848"
        question_1.add_answer(answer_2)
        questionnaire_1.register(answer_2)

        return questionnaire_1

    def _create_mock_answers_store(self):
        class MockAnswerStore(AbstractAnswerStore):
            def __init__(self):
                self._answers = {}

            def store_answer(self, key, value):
                self.answers[key] = value

            def get_answer(self, key):
                return self.answers[key] or None

            def get_answers(self, key):
                raise NotImplementedError()

            def clear(self):
                self._answers.clear()

            def clear_answers(self):
                self.clear();

        return MockAnswerStore()

    def _create_mock_validation_store(self):
        class MockValidationStore(AbstractValidationStore):
            def __init__(self):
                self.results = {}

            def store_result(self, key, value):
                self.results[key] = value

            def get_result(self, key):
                return self.results[key] or None

            def clear(self):
                self._answers.clear()

        return MockValidationStore()


class MockValidator(AbstractValidator):
    def __init__(self, success, message=None):
        self.success = success
        self.message = message

    def validate(self, user_answer):
        result = ValidationResult(self.success)
        if not self.success:
            result.errors.append(self.message)
        return result


class RaisingValidator(AbstractValidator):
    def validate(self, user_answer):
        raise Exception('validate called against \'{}\''.format(user_answer))


class MockTypeValidatorFactory(object):
    def get_validators_by_type(item):
        if item.type == "succeed":
            return [MockValidator(True)]
        elif item.type == 'except':
            return [RaisingValidator()]
        else:
            return [MockValidator(False, 'Validation Failed')]


class MockValidationStore(AbstractValidationStore):
    def __init__(self):
        self._store = {}

    def store_result(self, key, value):
        self._store[key] = value

    def get_result(self, key):
        return self._store[key] or None

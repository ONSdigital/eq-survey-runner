import unittest
from app.validation.type_validator_factory import TypeValidatorFactory, TypeValidatorFactoryException
from app.validation.integer_type_check import IntegerTypeCheck
from app.validation.date_type_check import DateTypeCheck
from app.schema.answer import Answer


class TypeValidatorFactoryTest(unittest.TestCase):
    def test_get_validators_by_type(self):

        item = Answer()
        item.type = 'integer'
        validators = TypeValidatorFactory.get_validators_by_type(item)

        self.assertEquals(len(validators), 1)
        self.assertTrue(isinstance(validators[0], IntegerTypeCheck))

        item.type = 'date'
        validators = TypeValidatorFactory.get_validators_by_type(item)

        self.assertEquals(len(validators), 1)
        self.assertTrue(isinstance(validators[0], DateTypeCheck))

        item.type = 'unknown_type'
        self.assertRaises(TypeValidatorFactoryException, TypeValidatorFactory.get_validators_by_type, item)

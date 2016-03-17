import unittest
from app.validation.type_validator_factory import TypeValidatorFactory, TypeValidatorFactoryException
from app.validation.integer_type_check import IntegerTypeCheck
from app.validation.date_type_check import DateTypeCheck


class TypeValidatorFactoryTest(unittest.TestCase):
    def test_get_validators_by_type(self):

        validators = TypeValidatorFactory.get_validators_by_type('integer')

        self.assertEquals(len(validators), 1)
        self.assertTrue(isinstance(validators[0], IntegerTypeCheck))

        validators = TypeValidatorFactory.get_validators_by_type('daterange')

        self.assertEquals(len(validators), 1)
        self.assertTrue(isinstance(validators[0], DateTypeCheck))

        self.assertRaises(TypeValidatorFactoryException, TypeValidatorFactory.get_validators_by_type, "unknown_type")

import unittest
from app.validation.type_validator_factory import TypeValidatorFactory, TypeValidatorFactoryException
from app.validation.integer import Integer


class TypeValidatorFactoryTest(unittest.TestCase):
    def test_get_validators_by_type(self):

        # Currently only Integer type is supported
        validators = TypeValidatorFactory.get_validators_by_type('integer')

        self.assertEquals(len(validators), 1)
        self.assertTrue(isinstance(validators[0], Integer))

        self.assertRaises(TypeValidatorFactoryException, TypeValidatorFactory.get_validators_by_type, "unknown_type")

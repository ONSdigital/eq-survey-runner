import unittest

from app.schema.answer import Answer
from app.schema.question import Question
from app.validation.date_range_check import DateRangeCheck
from app.validation.date_type_check import DateTypeCheck
from app.validation.integer_type_check import IntegerTypeCheck
from app.validation.positive_integer_type_check import PositiveIntegerTypeCheck
from app.validation.textarea_type_check import TextAreaTypeCheck
from app.validation.type_validator_factory import TypeValidatorFactory, TypeValidatorFactoryException


class TypeValidatorFactoryTest(unittest.TestCase):
    def test_get_known_validators_by_type(self):
        # answer types
        item = Answer()
        item.type = 'integer'
        validators = TypeValidatorFactory.get_validators_by_type(item)

        self.assertEqual(len(validators), 1)
        self.assertTrue(isinstance(validators[0], IntegerTypeCheck))

        item.type = 'date'
        validators = TypeValidatorFactory.get_validators_by_type(item)

        self.assertEqual(len(validators), 1)
        self.assertTrue(isinstance(validators[0], DateTypeCheck))

        item.type = 'positiveinteger'
        validators = TypeValidatorFactory.get_validators_by_type(item)

        self.assertEqual(len(validators), 1)
        self.assertTrue(isinstance(validators[0], PositiveIntegerTypeCheck))

        item.type = 'textarea'
        validators = TypeValidatorFactory.get_validators_by_type(item)

        self.assertEqual(len(validators), 1)
        self.assertTrue(isinstance(validators[0], TextAreaTypeCheck))

        # question types
        item = Question()

        item.type = 'daterange'
        validators = TypeValidatorFactory.get_validators_by_type(item)

        self.assertEqual(len(validators), 1)
        self.assertTrue(isinstance(validators[0], DateRangeCheck))

    def test_unknown_validators(self):
        # answer types
        item = Answer()

        item.type = 'unknown_type'
        self.assertRaises(TypeValidatorFactoryException, TypeValidatorFactory.get_validators_by_type, item)

        # question types
        item = Question()

        item.type = 'unknown_type'
        self.assertRaises(TypeValidatorFactoryException, TypeValidatorFactory.get_validators_by_type, item)

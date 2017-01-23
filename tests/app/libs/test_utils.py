import unittest

from app.libs.utils import ObjectFromDict


class ObjectFromDictTest(unittest.TestCase):
    def test_simple_object(self):
        simple_dict = {
            'property_one': 'string',
            'property_two': 2,
            'property_three': []
        }

        obj = ObjectFromDict(simple_dict)

        # pylint: disable=maybe-no-member
        # Object is dynamically built and properties dynamically assigned
        self.assertEqual(obj.property_one, 'string')
        self.assertEqual(obj.property_two, 2)
        self.assertEqual(len(obj.property_three), 0)

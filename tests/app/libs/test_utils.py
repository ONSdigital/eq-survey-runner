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

        self.assertEquals(obj.property_one, 'string')
        self.assertEquals(obj.property_two, 2)
        self.assertEquals(len(obj.property_three), 0)

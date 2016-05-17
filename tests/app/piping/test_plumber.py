from app.piping.plumber import Plumber
from datetime import datetime
import unittest


# Helper class to creata an object from a dict
class ObjectFromDict:
    def __init__(self, dict):
        self.__dict__ = dict


class TestPlumber(unittest.TestCase):
    def setUp(self):
        context_dict = {
            "simple": ObjectFromDict({
                "property_one": "value one",
                "property_two": "value two"
            }),
            'dates': ObjectFromDict({
                "first_april_2016": datetime.strptime('01-04-2016', "%d-%m-%Y")
            })
        }

        self.plumber = Plumber(context_dict)

    def test_plumb_item(self):
        item = ObjectFromDict({
            "templatable_properties": ['description'],
            "description": "Property One is {simple.property_one}, while Property Two is {simple.property_two}"
        })

        self.assertEquals(item.description, "Property One is {simple.property_one}, while Property Two is {simple.property_two}")

        self.plumber.plumb_item(item)

        self.assertEquals(item.description, "Property One is value one, while Property Two is value two")

        item2 = ObjectFromDict({
            "templatable_properties": ['property_one', 'property_two', 'property_three'],
            "property_one": "Date is {dates.first_april_2016:%-d %B %Y}",
            "property_two": "Date is {dates.first_april_2016:%Y/%m/%d}",
            "property_three": "Date is {dates.first_april_2016}",
            "property_four": "Not plumbed {dates.first_april_2016}"
        })

        self.assertEquals(item2.property_one, "Date is {dates.first_april_2016:%-d %B %Y}")
        self.assertEquals(item2.property_two, "Date is {dates.first_april_2016:%Y/%m/%d}")
        self.assertEquals(item2.property_three, "Date is {dates.first_april_2016}")
        self.assertEquals(item2.property_four, "Not plumbed {dates.first_april_2016}")

        self.plumber.plumb_item(item2)

        self.assertEquals(item2.property_one, "Date is 1 April 2016")
        self.assertEquals(item2.property_two, "Date is 2016/04/01")
        self.assertEquals(item2.property_three, "Date is 2016-04-01 00:00:00")
        self.assertEquals(item2.property_four, "Not plumbed {dates.first_april_2016}")

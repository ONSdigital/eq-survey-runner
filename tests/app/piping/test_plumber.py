from app.piping.plumber import Plumber
from datetime import datetime
import unittest
from app.libs.utils import ObjectFromDict


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

        item3 = ObjectFromDict({
            'templatable_properties': ['funky_formatting', 'random_brace', 'mixing_it_up'],
            'funky_formatting': 'This is an opening brace {{ and this is a closing brace }}',
            'random_brace': 'This will not throw an error {',
            'mixing_it_up': '{{ {simple.property_one} {simple.property_two} }}'
        })

        self.assertEquals(item3.funky_formatting, 'This is an opening brace {{ and this is a closing brace }}')
        self.assertEquals(item3.random_brace, 'This will not throw an error {')
        self.assertEquals(item3.mixing_it_up, '{{ {simple.property_one} {simple.property_two} }}')

        self.plumber.plumb_item(item3)

        self.assertEquals(item3.funky_formatting, 'This is an opening brace { and this is a closing brace }')
        self.assertEquals(item3.random_brace, 'This will not throw an error {')
        self.assertEquals(item3.mixing_it_up, '{ value one value two }')

        item4 = ObjectFromDict({
            'templatable_properties': ['unknown_parameter'],
            'unknown_parameter': 'This expansion is {unknown}'
        })

        self.assertEquals(item4.unknown_parameter, 'This expansion is {unknown}')

        self.plumber.plumb_item(item4)

        self.assertEquals(item4.unknown_parameter, 'This expansion is {unknown}')

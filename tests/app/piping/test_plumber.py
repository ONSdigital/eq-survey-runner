from mock import patch

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
                "first_april_2016": datetime.strptime('01-04-2016', "%d-%m-%Y"),
                'none_date': None
            })
        }

        self.plumber = Plumber(context_dict)

    def test_plumb_item(self):
        item = ObjectFromDict({
            "id": "item1",
            "templatable_properties": ['description'],
            "description": "Property One is {{simple.property_one}}, while Property Two is {{simple.property_two}}"
        })

        with patch('app.piping.plumber.render_template_string', return_value="Property One is value one, while Property Two is value two"):
            self.plumber.plumb_item(item)

        self.assertEquals(item.description, "Property One is value one, while Property Two is value two")

import unittest

from app.questionnaire.placeholder_transforms import PlaceholderTransforms


class TestPlaceholderParser(unittest.TestCase):
    def setUp(self):
        self.transforms = PlaceholderTransforms()

    def test_format_currency(self):
        assert self.transforms.format_currency('11', 'GBP') == '£11.00'
        assert self.transforms.format_currency('11.99', 'GBP') == '£11.99'
        assert self.transforms.format_currency('11000', 'USD') == 'US$11,000.00'
        assert self.transforms.format_currency(0) == '£0.00'
        assert self.transforms.format_currency(0.00) == '£0.00'

    def test_format_number(self):
        assert self.transforms.format_number(123) == '123'
        assert self.transforms.format_number('123.4') == '123.4'
        assert self.transforms.format_number('123.40') == '123.4'
        assert self.transforms.format_number('1000') == '1,000'
        assert self.transforms.format_number('10000') == '10,000'
        assert self.transforms.format_number('100000000') == '100,000,000'
        assert self.transforms.format_number(0) == '0'
        assert self.transforms.format_number(0.00) == '0'
        assert self.transforms.format_number('') == ''
        assert self.transforms.format_number(None) == ''

    def test_format_list(self):
        names = [
            'Alice Aardvark', 'Bob Berty Brown', 'Dave Dixon Davies'
        ]

        format_value = self.transforms.format_list(names)

        expected_result = '<ul>' \
                          '<li>Alice Aardvark</li>' \
                          '<li>Bob Berty Brown</li>' \
                          '<li>Dave Dixon Davies</li>' \
                          '</ul>'

        assert expected_result == format_value

    def test_format_possessive(self):
        assert self.transforms.format_possessive('Alice Aardvark') == 'Alice Aardvark’s'
        assert self.transforms.format_possessive('Dave Dixon Davies') == 'Dave Dixon Davies’'
        assert self.transforms.format_possessive("Alice Aardvark's") == 'Alice Aardvark’s'
        assert self.transforms.format_possessive('Alice Aardvark’s') == 'Alice Aardvark’s'

    def test_calculate_years_difference(self):
        assert self.transforms.calculate_years_difference('2016-06-10', '2019-06-10') == '3'
        assert self.transforms.calculate_years_difference('2010-01-01', '2018-12-31') == '8'
        assert self.transforms.calculate_years_difference('now', 'now') == '0'

    def test_concatenate_list(self):
        list_to_concatenate = ['Milk', 'Eggs', 'Flour', 'Water']

        assert self.transforms.concatenate_list(list_to_concatenate, '') == 'MilkEggsFlourWater'
        assert self.transforms.concatenate_list(list_to_concatenate, ' ') == 'Milk Eggs Flour Water'
        assert self.transforms.concatenate_list(list_to_concatenate, ', ') == 'Milk, Eggs, Flour, Water'

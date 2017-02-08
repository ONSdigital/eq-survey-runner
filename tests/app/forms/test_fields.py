import unittest

from wtforms import validators, StringField, TextAreaField, FormField, SelectField, SelectMultipleField

from app.forms.fields import CustomIntegerField, get_field, get_mandatory_validator
from app.validation.error_messages import error_messages


class TestFields(unittest.TestCase):

    def test_get_mandatory_validator_optional(self):
        answer = {
            'mandatory': False
        }
        validate_with = get_mandatory_validator(answer, None)

        self.assertIsInstance(validate_with[0], validators.Optional)

    def test_get_mandatory_validator_mandatory(self):
        answer = {
            'mandatory': True
        }
        validate_with = get_mandatory_validator(answer, {
            'MANDATORY': 'This is the default mandatory message'
        })

        self.assertIsInstance(validate_with[0], validators.InputRequired)
        self.assertEqual(validate_with[0].message, 'This is the default mandatory message')

    def test_get_mandatory_validator_mandatory_with_error(self):
        answer = {
            'mandatory': True,
            'validation': {
                'messages': {
                    'MANDATORY': 'This is the mandatory message for an answer'
                }
            }
        }
        validate_with = get_mandatory_validator(answer, {
            'MANDATORY': 'This is the default mandatory message'
        })

        self.assertIsInstance(validate_with[0], validators.InputRequired)
        self.assertEqual(validate_with[0].message, 'This is the mandatory message for an answer')

    def test_string_field(self):
        textfield_json = {
            "id": "job-title-answer",
            "label": "Job title",
            "mandatory": False,
            "guidance": "<p>Please enter your job title in the space provided.</p>",
            "type": "TextField"
        }
        unbound_field = get_field(textfield_json, textfield_json['label'], error_messages)

        self.assertTrue(unbound_field.field_class == StringField)
        self.assertEquals(unbound_field.kwargs['label'], textfield_json['label'])
        self.assertEquals(unbound_field.kwargs['description'], textfield_json['guidance'])

    def test_text_area_field(self):
        textarea_json = {
            "guidance": "",
            "id": "answer",
            "label": "Enter your comments",
            "mandatory": False,
            "q_code": "0",
            "type": "TextArea"
        }

        unbound_field = get_field(textarea_json, textarea_json['label'], error_messages)

        self.assertTrue(unbound_field.field_class == TextAreaField)
        self.assertEquals(unbound_field.kwargs['label'], textarea_json['label'])
        self.assertEquals(unbound_field.kwargs['description'], textarea_json['guidance'])

    def test_date_field(self):
        date_json = {
            "guidance": "Please enter a date",
            "id": "period-to",
            "label": "Period to",
            "mandatory": True,
            "type": "Date",
            "validation": {
                "messages": {
                    "INVALID_DATE": "The date entered is not valid.  Please correct your answer.",
                    "MANDATORY": "Please provide an answer to continue."
                }
            }
        }

        unbound_field = get_field(date_json, date_json['label'], error_messages)

        self.assertTrue(unbound_field.field_class == FormField)
        self.assertEquals(unbound_field.kwargs['label'], date_json['label'])
        self.assertEquals(unbound_field.kwargs['description'], date_json['guidance'])

    def test_month_year_date_field(self):
        date_json = {
            "guidance": "",
            "id": "month-year-answer",
            "label": "Date",
            "mandatory": True,
            "options": [],
            "q_code": "11",
            "type": "MonthYearDate",
            "validation": {
                "messages": {
                    "INVALID_DATE": "The date entered is not valid.  Please correct your answer.",
                    "MANDATORY": "Please provide an answer to continue."
                }
            }
        }

        unbound_field = get_field(date_json, date_json['label'], error_messages)

        self.assertTrue(unbound_field.field_class == FormField)
        self.assertEquals(unbound_field.kwargs['label'], date_json['label'])
        self.assertEquals(unbound_field.kwargs['description'], date_json['guidance'])

    def test_radio_field(self):
        radio_json = {
            "guidance": "",
            "id": "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c",
            "label": "Choose a side",
            "mandatory": True,
            "options": [
                {
                    "label": "Light Side",
                    "value": "Light Side",
                    "description": "The light side of the Force"
                },
                {
                    "label": "Dark Side",
                    "value": "Dark Side",
                    "description": "The dark side of the Force"
                },
                {
                    "label": "I prefer Star Trek",
                    "value": "I prefer Star Trek"
                },
                {
                    "label": "Other",
                    "value": "Other"
                }
            ],
            "q_code": "20",
            "type": "Radio"
        }

        unbound_field = get_field(radio_json, radio_json['label'], error_messages)

        expected_choices = [(option['label'], option['value']) for option in radio_json['options']]

        self.assertTrue(unbound_field.field_class == SelectField)
        self.assertEquals(unbound_field.kwargs['label'], radio_json['label'])
        self.assertEquals(unbound_field.kwargs['description'], radio_json['guidance'])
        self.assertEquals(unbound_field.kwargs['choices'], expected_choices)

    def test_checkbox_field(self):
        checkbox_json = {
            "guidance": "",
            "id": "5587eb9b-f24e-4dc0-ac94-66117b896c10",
            "label": "",
            "mandatory": False,
            "options": [
                {
                    "label": "Luke Skywalker",
                    "value": "Luke Skywalker"
                },
                {
                    "label": "Han Solo",
                    "value": "Han Solo"
                },
                {
                    "label": "The Emperor",
                    "value": "The Emperor"
                },
                {
                    "label": "R2D2",
                    "value": "R2D2"
                },
                {
                    "label": "Senator Amidala",
                    "value": "Senator Amidala"
                },
                {
                    "label": "Yoda",
                    "value": "Yoda"
                }
            ],
            "q_code": "7",
            "type": "Checkbox"
        }

        unbound_field = get_field(checkbox_json, checkbox_json['label'], error_messages)

        expected_choices = [(option['label'], option['value']) for option in checkbox_json['options']]

        self.assertTrue(unbound_field.field_class == SelectMultipleField)
        self.assertEquals(unbound_field.kwargs['label'], checkbox_json['label'])
        self.assertEquals(unbound_field.kwargs['description'], checkbox_json['guidance'])
        self.assertEquals(unbound_field.kwargs['choices'], expected_choices)

    def test_integer_field(self):
        integer_json = {
            "alias": "chewies_age",
            "guidance": "",
            "id": "6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b",
            "label": "How old is Chewy?",
            "mandatory": True,
            "q_code": "1",
            "type": "Integer",
            "validation": {
                "messages": {
                    "INTEGER_TOO_LARGE": "No one lives that long, not even Yoda",
                    "NEGATIVE_INTEGER": "Negative age you can not be.",
                    "NOT_INTEGER": "Please enter your age."
                }
            }
        }

        unbound_field = get_field(integer_json, integer_json['label'], error_messages)

        self.assertTrue(unbound_field.field_class == CustomIntegerField)
        self.assertEquals(unbound_field.kwargs['label'], integer_json['label'])
        self.assertEquals(unbound_field.kwargs['description'], integer_json['guidance'])

    def test_positive_integer_field(self):
        integer_json = {
            "guidance": "",
            "id": "pre49d93-cbdc-4bcb-adb2-0e0af6c9a07c",
            "label": "How hot is a lightsaber in degrees C?",
            "mandatory": False,
            "type": "PositiveInteger",
            "validation": {
                "messages": {
                    "INTEGER_TOO_LARGE": "Thats hotter then the sun, Jar Jar Binks you must be",
                    "NEGATIVE_INTEGER": "How can it be negative?",
                    "NOT_INTEGER": "Please only enter whole numbers into the field."
                }
            }
        }

        unbound_field = get_field(integer_json, integer_json['label'], error_messages)

        self.assertTrue(unbound_field.field_class == CustomIntegerField)
        self.assertEquals(unbound_field.kwargs['label'], integer_json['label'])
        self.assertEquals(unbound_field.kwargs['description'], integer_json['guidance'])

    def test_currency_field(self):
        currency_json = {
            "guidance": "",
            "id": "a04a516d-502d-4068-bbed-a43427c68cd9",
            "label": "",
            "mandatory": True,
            "q_code": "2",
            "type": "Currency",
            "validation": {
                "messages": {
                    "INTEGER_TOO_LARGE": "How much, fool you must be",
                    "NEGATIVE_INTEGER": "How can it be negative?",
                    "NOT_INTEGER": "Please only enter whole numbers into the field."
                }
            }
        }

        unbound_field = get_field(currency_json, currency_json['label'], error_messages)

        self.assertTrue(unbound_field.field_class == CustomIntegerField)
        self.assertEquals(unbound_field.kwargs['label'], currency_json['label'])
        self.assertEquals(unbound_field.kwargs['description'], currency_json['guidance'])

    def test_percentage_field(self):
        percentage_json = {
            "description": "",
            "id": "percentage-turnover-2016-market-new-answer",
            "label": "New to the market in 2014-2016",
            "mandatory": False,
            "q_code": "0810",
            "type": "Percentage",
            "validation": {
                "messages" : {
                    "INTEGER_TOO_LARGE": "The maximum value allowed is 100. Please correct your answer."
                }
            }
        }

        unbound_field = get_field(percentage_json, percentage_json['label'], error_messages)

        self.assertTrue(unbound_field.field_class == CustomIntegerField)
        self.assertEquals(unbound_field.kwargs['label'], percentage_json['label'])
        self.assertEquals(unbound_field.kwargs['description'], percentage_json['description'])

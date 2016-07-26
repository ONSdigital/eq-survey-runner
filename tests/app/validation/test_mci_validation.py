"""
This is more of an integration test than a unit test.  It loads the MCI Schema,
parses it and then tests the validation rules needed before MCI can go live.
"""
import unittest

from app.schema_loader import schema_loader
from app.parser.schema_parser_factory import SchemaParserFactory


class ValidatorTest(unittest.TestCase):
    def setUp(self):

        self._answer_store = self._create_mock_answers_store()
        self._validation_store = self._create_mock_validation_store()
        self._schema = self._create_schema()

        self.ids = {
            "REPORTING_PERIOD_START": "6fd644b0-798e-4a58-a393-a438b32fe637",
            "REPORTING_PERIOD_END": "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0",
            "TOTAL_RETAIL_TURNOVER": "e81adc6d-6fb0-4155-969c-d0d646f15345",
            "INTERNET_SALES": "4b75a6f7-9774-4b2b-82dc-976561189a99",
            "FUEL_SALES": "b2bac3ed-5504-43ef-a883-f9ca8496aca3",
            "SALES_PERIOD": "6cc86b54-330c-4465-99b2-34cc7073dc2c"
        }

    def test_validate_empty_questionnaire(self):
        validator = Validator(self._schema, self._validation_store, self._answer_store)

        # Clear the answer store and validation store
        self._answer_store.clear()
        self._validation_store.clear()

        # setup blank answers for all required fields
        self._answer_store.store_answer(self.ids['REPORTING_PERIOD_START'], '')
        self._answer_store.store_answer(self.ids['REPORTING_PERIOD_END'], '')
        self._answer_store.store_answer(self.ids['TOTAL_RETAIL_TURNOVER'], '')
        self._answer_store.store_answer(self.ids['INTERNET_SALES'], '')
        self._answer_store.store_answer(self.ids['FUEL_SALES'], '')

        # validate the questionnaire
        validator.validate(self._answer_store.get_answers())

        # Period Start Tests
        period_start_result = self._validation_store.get_result(self.ids['REPORTING_PERIOD_START'])

        self.assertFalse(period_start_result.is_valid)
        self.assertEquals(len(period_start_result.errors), 1)
        self.assertEquals(period_start_result.errors[0], 'Please answer before continuing.')
        self.assertEquals(len(period_start_result.warnings), 0)

        # Period End Tests
        period_end_result = self._validation_store.get_result(self.ids['REPORTING_PERIOD_END'])

        self.assertFalse(period_end_result.is_valid)
        self.assertEquals(len(period_end_result.errors), 1)
        self.assertEquals(period_end_result.errors[0], 'Please answer before continuing.')
        self.assertEquals(len(period_end_result.warnings), 0)

        # Total Retail Turnover Tests
        total_turnover_result = self._validation_store.get_result(self.ids['TOTAL_RETAIL_TURNOVER'])

        self.assertFalse(total_turnover_result.is_valid)
        self.assertEquals(len(total_turnover_result.errors), 1)
        self.assertEquals(total_turnover_result.errors[0], 'Please provide a value, even if your value is 0.')
        self.assertEquals(len(total_turnover_result.warnings), 0)

        # Internet Sales Tests
        internet_sales_result = self._validation_store.get_result(self.ids['INTERNET_SALES'])

        # Internet Sales is not-mandatory
        self.assertTrue(internet_sales_result.is_valid)
        self.assertEquals(len(internet_sales_result.errors), 0)
        self.assertEquals(len(internet_sales_result.warnings), 0)

        # Fuel Sales Tests
        fuel_sales_result = self._validation_store.get_result(self.ids['FUEL_SALES'])

        # Fuel Sales is not-mandatory
        self.assertTrue(fuel_sales_result.is_valid)
        self.assertEquals(len(fuel_sales_result.errors), 0)
        self.assertEquals(len(fuel_sales_result.warnings), 0)

    def test_invalid_dates(self):
        validator = Validator(self._schema, self._validation_store, self._answer_store)

        # Clear the answer store and validation store
        self._answer_store.clear()
        self._validation_store.clear()

        # setup invalid dates for date fields
        self._answer_store.store_answer(self.ids['REPORTING_PERIOD_START'], '13/13/2013')
        self._answer_store.store_answer(self.ids['REPORTING_PERIOD_END'], '29/02/2015')

        # validate the questionnaire
        validator.validate(self._answer_store.get_answers())

        # Period Start Tests
        period_start_result = self._validation_store.get_result(self.ids['REPORTING_PERIOD_START'])

        self.assertFalse(period_start_result.is_valid)
        self.assertEquals(len(period_start_result.errors), 1)
        self.assertEquals(period_start_result.errors[0], 'The date entered is not valid.  Please correct your answer.')
        self.assertEquals(len(period_start_result.warnings), 0)

        # Period End Tests
        period_end_result = self._validation_store.get_result(self.ids['REPORTING_PERIOD_END'])

        self.assertFalse(period_end_result.is_valid)
        self.assertEquals(len(period_end_result.errors), 1)
        self.assertEquals(period_end_result.errors[0], 'The date entered is not valid.  Please correct your answer.')
        self.assertEquals(len(period_end_result.warnings), 0)

    def test_invalid_date_diff(self):
        validator = Validator(self._schema, self._validation_store, self._answer_store)

        # Clear the answer store and validation store
        self._answer_store.clear()
        self._validation_store.clear()

        # setup invalid dates diff
        self._answer_store.store_answer(self.ids['REPORTING_PERIOD_START'], '01/01/2016')
        self._answer_store.store_answer(self.ids['REPORTING_PERIOD_END'], '01/01/2016')

        # validate the questionnaire
        validator.validate(self._answer_store.get_answers())

        # Period Tests
        period_start_result = self._validation_store.get_result(self.ids['SALES_PERIOD'])

        self.assertFalse(period_start_result.is_valid)
        self.assertEquals(len(period_start_result.errors), 1)
        self.assertEquals(period_start_result.errors[0], "The 'to' date must be different to the 'from' date.")
        self.assertEquals(len(period_start_result.warnings), 0)

    def test_invalid_date_diff_range(self):
        validator = Validator(self._schema, self._validation_store, self._answer_store)

        # Clear the answer store and validation store
        self._answer_store.clear()
        self._validation_store.clear()

        # setup invalid date diff
        self._answer_store.store_answer(self.ids['REPORTING_PERIOD_START'], '01/01/2017')
        self._answer_store.store_answer(self.ids['REPORTING_PERIOD_END'], '01/01/2016')

        # validate the questionnaire
        validator.validate(self._answer_store.get_answers())

        # Period Tests
        period_start_result = self._validation_store.get_result(self.ids['SALES_PERIOD'])

        self.assertFalse(period_start_result.is_valid)
        self.assertEquals(len(period_start_result.errors), 1)
        self.assertEquals(period_start_result.errors[0], "The 'to' date cannot be before the 'from' date.")
        self.assertEquals(len(period_start_result.warnings), 0)


    def test_invalid_total_turnover(self):
        validator = Validator(self._schema, self._validation_store, self._answer_store)

        # Clear the answer store and validation store
        self._answer_store.clear()
        self._validation_store.clear()

        # setup invalid total
        self._answer_store.store_answer(self.ids['TOTAL_RETAIL_TURNOVER'], 'This is invalid')

        # validate the questionnaire
        validator.validate(self._answer_store.get_answers())

        # Total Retail Turnover Tests
        total_turnover_result = self._validation_store.get_result(self.ids['TOTAL_RETAIL_TURNOVER'])

        self.assertFalse(total_turnover_result.is_valid)
        self.assertEquals(len(total_turnover_result.errors), 1)
        self.assertEquals(total_turnover_result.errors[0], 'Please only enter whole numbers into the field.')
        self.assertEquals(len(total_turnover_result.warnings), 0)


        # Clear the answer store and validation store
        self._answer_store.clear()
        self._validation_store.clear()

        # setup invalid total
        self._answer_store.store_answer(self.ids['TOTAL_RETAIL_TURNOVER'], '-1')

        # validate the questionnaire
        validator.validate(self._answer_store.get_answers())

        # Total Retail Turnover Tests
        total_turnover_result = self._validation_store.get_result(self.ids['TOTAL_RETAIL_TURNOVER'])

        self.assertFalse(total_turnover_result.is_valid)
        self.assertEquals(len(total_turnover_result.errors), 1)
        self.assertEquals(total_turnover_result.errors[0], 'The value cannot be negative. Please correct your answer.')
        self.assertEquals(len(total_turnover_result.warnings), 0)

    def test_invalid_fuel_sales(self):
        validator = Validator(self._schema, self._validation_store, self._answer_store)

        # Clear the answer store and validation store
        self._answer_store.clear()
        self._validation_store.clear()

        # setup invalid fuel sales
        self._answer_store.store_answer(self.ids['FUEL_SALES'], 'not numeric')

        # validate the questionnaire
        validator.validate(self._answer_store.get_answers())

        # Fuel Sales Tests
        fuel_sales_result = self._validation_store.get_result(self.ids['FUEL_SALES'])

        self.assertFalse(fuel_sales_result.is_valid)
        self.assertEquals(len(fuel_sales_result.errors), 1)
        self.assertEquals(fuel_sales_result.errors[0], 'Please only enter whole numbers into the field.')
        self.assertEquals(len(fuel_sales_result.warnings), 0)


        # Clear the answer store and validation store
        self._answer_store.clear()
        self._validation_store.clear()

        # setup negative fuel sales
        self._answer_store.store_answer(self.ids['FUEL_SALES'], '-1')

        # validate the questionnaire
        validator.validate(self._answer_store.get_answers())

        # Fuel Sales Tests
        fuel_sales_result = self._validation_store.get_result(self.ids['FUEL_SALES'])

        self.assertFalse(fuel_sales_result.is_valid)
        self.assertEquals(len(fuel_sales_result.errors), 1)
        self.assertEquals(fuel_sales_result.errors[0], 'The value cannot be negative. Please correct your answer.')
        self.assertEquals(len(fuel_sales_result.warnings), 0)

    def test_invalid_internet_sales(self):
        validator = Validator(self._schema, self._validation_store, self._answer_store)

        # Clear the answer store and validation store
        self._answer_store.clear()
        self._validation_store.clear()

        # setup negative internet sales
        self._answer_store.store_answer(self.ids['INTERNET_SALES'], '-1')

        # validate the questionnaire
        validator.validate(self._answer_store.get_answers())

        # Internet Sales Tests
        internet_sales_result = self._validation_store.get_result(self.ids['INTERNET_SALES'])

        self.assertFalse(internet_sales_result.is_valid)
        self.assertEquals(len(internet_sales_result.errors), 1)
        self.assertEquals(internet_sales_result.errors[0], 'The value cannot be negative. Please correct your answer.')
        self.assertEquals(len(internet_sales_result.warnings), 0)


    def _create_schema(self):
        # Load the actual MCI Schema, ...
        schema = schema_loader.load_schema("1", "0205")
        # ... parse it ....
        parser = SchemaParserFactory.create_parser(schema)
        questionnaire = parser.parse()
        # ... and return it
        return questionnaire

    def _create_mock_answers_store(self):
        class MockAnswerStore(object):
            def __init__(self):
                self.answers = {}

            def store_answer(self, key, value):
                self.answers[key] = value

            def get_answer(self, key):
                if key in self.answers.keys():
                    return self.answers[key]
                else:
                    return None

            def get_answers(self):
                return self.answers

            def clear(self):
                self.answers.clear()

            def clear_answers(self):
                self.clear();

        return MockAnswerStore()

    def _create_mock_validation_store(self):
        class MockValidationStore(AbstractValidationStore):
            def __init__(self):
                self.results = {}

            def store_result(self, key, value):
                self.results[key] = value

            def get_result(self, key):
                if key in self.results.keys():
                    return self.results[key]
                else:
                    return None

            def clear(self):
                self.results.clear()

        return MockValidationStore()

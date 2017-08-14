from wtforms import validators

from app.forms.household_composition_form import generate_household_composition_form, deserialise_composition_answers
from app.validation.validators import ResponseRequired
from app.utilities.schema import load_schema_file
from app.helpers.schema_helper import SchemaHelper
from app.questionnaire.location import Location

from tests.app.app_context_test_case import AppContextTestCase


class TestHouseholdCompositionForm(AppContextTestCase):
    def setUp(self):
        super().setUp()

        survey = load_schema_file("census_household.json")
        self.block_json = SchemaHelper.get_block(survey, 'household-composition')
        self.error_messages = SchemaHelper.get_messages(survey)

    @staticmethod
    def _error_exists(answer_id, msg, mapped_errors):
        return any(a_id == answer_id and msg in ordered_errors for a_id, ordered_errors in mapped_errors)

    def test_get_name_form_generates_name_form(self):
        with self.test_request_context():
            form = generate_household_composition_form(self.block_json, {}, error_messages=self.error_messages)

            self.assertEqual(len(form.household.entries), 1)

            first_name_field = getattr(form.household.entries[0], 'first-name')
            middle_names_field = getattr(form.household.entries[0], 'middle-names')
            last_name_field = getattr(form.household.entries[0], 'last-name')

            self.assertIsInstance(first_name_field.validators[0], ResponseRequired)
            self.assertIsInstance(middle_names_field.validators[0], validators.Optional)
            self.assertIsInstance(last_name_field.validators[0], validators.Optional)

    def test_form_errors_are_correctly_mapped(self):
        with self.test_request_context():
            form = generate_household_composition_form(self.block_json, {}, error_messages=self.error_messages)

            form.validate()

            message = "Please enter a name or remove the person to continue"

            self.assertTrue(self._error_exists('household-0-first-name', message, form.map_errors()))

    def test_answer_errors_are_mapped(self):
        with self.test_request_context():
            form = generate_household_composition_form(self.block_json, {}, error_messages=self.error_messages)

            form.validate()

            message = "Please enter a name or remove the person to continue"

            self.assertIn(message, form.answer_errors('household-0-first-name'))

    def test_form_creation_with_data(self):
        with self.test_request_context():
            form = generate_household_composition_form(self.block_json, {
                'household-0-first-name': 'Joe',
                'household-0-last-name': 'Bloggs',
                'household-1-first-name': 'Jane',
                'household-1-last-name': 'Seymour',
            }, error_messages=self.error_messages)

            self.assertEqual(len(form.household.entries), 2)
            self.assertEqual(form.household.entries[0].data, {
                'first-name': 'Joe',
                'middle-names': '',
                'last-name': 'Bloggs'
            })
            self.assertEqual(form.household.entries[1].data, {
                'first-name': 'Jane',
                'middle-names': '',
                'last-name': 'Seymour'
            })

    def test_whitespace_in_first_name_invalid(self):
        with self.test_request_context():
            form = generate_household_composition_form(self.block_json, {
                'household-0-first-name': '     ',
                'household-0-last-name': 'Bloggs',
            }, error_messages=self.error_messages)

            form.validate()

            message = "Please enter a name or remove the person to continue"

            self.assertIn(message, form.answer_errors('household-0-first-name'))

    def test_remove_first_person(self):
        with self.test_request_context():
            form = generate_household_composition_form(self.block_json, {
                'household-0-first-name': 'Joe',
                'household-0-last-name': 'Bloggs',
                'household-1-first-name': 'Bob',
                'household-1-middle-names': 'Michael',
                'household-1-last-name': 'Seymour',
                'household-2-first-name': 'Sophie',
                'household-2-last-name': 'Bloggs',
                'household-3-first-name': 'Jane',
                'household-3-last-name': 'Seymour',
            }, error_messages=self.error_messages)

            form.remove_person(0)

            self.assertEqual(len(form.household.entries), 3)
            self.assertEqual(form.household.entries[0].data, {

                'first-name': 'Bob',
                'middle-names': 'Michael',
                'last-name': 'Seymour'
            })
            self.assertEqual(form.household.entries[1].data, {
                'first-name': 'Sophie',
                'middle-names': '',
                'last-name': 'Bloggs'
            })
            self.assertEqual(form.household.entries[2].data, {
                'first-name': 'Jane',
                'middle-names': '',
                'last-name': 'Seymour'
            })

    def test_remove_middle_person(self):
        with self.test_request_context():
            form = generate_household_composition_form(self.block_json, {
                'household-0-first-name': 'Joe',
                'household-0-last-name': 'Bloggs',
                'household-1-first-name': 'Bob',
                'household-1-middle-names': 'Michael',
                'household-1-last-name': 'Seymour',
                'household-2-first-name': 'Sophie',
                'household-2-last-name': 'Bloggs',
                'household-3-first-name': 'Jane',
                'household-3-last-name': 'Seymour',
            }, error_messages=self.error_messages)

            form.remove_person(2)

            self.assertEqual(len(form.household.entries), 3)
            self.assertEqual(form.household.entries[0].data, {
                'first-name': 'Joe',
                'middle-names': '',
                'last-name': 'Bloggs'
            })
            self.assertEqual(form.household.entries[1].data, {
                'first-name': 'Bob',
                'middle-names': 'Michael',
                'last-name': 'Seymour'
            })
            self.assertEqual(form.household.entries[2].data, {
                'first-name': 'Jane',
                'middle-names': '',
                'last-name': 'Seymour'
            })

    def test_remove_last_person(self):
        with self.test_request_context():
            form = generate_household_composition_form(self.block_json, {
                'household-0-first-name': 'Joe',
                'household-0-last-name': 'Bloggs',
                'household-1-first-name': 'Bob',
                'household-1-last-name': 'Seymour',
                'household-2-first-name': 'Jane',
                'household-2-last-name': 'Seymour',
            }, error_messages=self.error_messages)

            form.remove_person(2)

            self.assertEqual(len(form.household.entries), 2)
            self.assertEqual(form.household.entries[0].data, {
                'first-name': 'Joe',
                'middle-names': '',
                'last-name': 'Bloggs'
            })
            self.assertEqual(form.household.entries[1].data, {
                'first-name': 'Bob',
                'middle-names': '',
                'last-name': 'Seymour'
            })

    def test_remove_person(self):
        with self.test_request_context():
            form = generate_household_composition_form(self.block_json, {
                'household-0-first-name': 'Joe',
                'household-0-last-name': 'Bloggs',
                'household-1-first-name': 'Bob',
                'household-1-last-name': 'Seymour',
            }, error_messages=self.error_messages)

            self.assertEqual(len(form.household.entries), 2)

            with self.assertRaises(IndexError):
                form.remove_person(3)

    def test_serialise_answers(self):
        with self.test_request_context():
            form = generate_household_composition_form(self.block_json, {
                'household-0-first-name': 'Joe',
                'household-0-last-name': 'Bloggs',
                'household-1-first-name': 'Bob',
                'household-1-last-name': 'Seymour',
            }, error_messages=self.error_messages)

            location = Location('who-lives-here', 0, 'household-composition')

            answers = form.serialise(location)

            expected_answers = [
                {
                    'group_id': 'who-lives-here',
                    'group_instance': 0,
                    'block_id': 'household-composition',
                    'answer_id': 'first-name',
                    'answer_instance': 0,
                    'value': 'Joe'
                }, {
                    'group_id': 'who-lives-here',
                    'group_instance': 0,
                    'block_id': 'household-composition',
                    'answer_id': 'middle-names',
                    'answer_instance': 0,
                    'value': ''
                }, {
                    'group_id': 'who-lives-here',
                    'group_instance': 0,
                    'block_id': 'household-composition',
                    'answer_id': 'last-name',
                    'answer_instance': 0,
                    'value': 'Bloggs'
                }, {
                    'group_id': 'who-lives-here',
                    'group_instance': 0,
                    'block_id': 'household-composition',
                    'answer_id': 'first-name',
                    'answer_instance': 1,
                    'value': 'Bob'
                }, {
                    'group_id': 'who-lives-here',
                    'group_instance': 0,
                    'block_id': 'household-composition',
                    'answer_id': 'middle-names',
                    'answer_instance': 1,
                    'value': ''
                }, {
                    'group_id': 'who-lives-here',
                    'group_instance': 0,
                    'block_id': 'household-composition',
                    'answer_id': 'last-name',
                    'answer_instance': 1,
                    'value': 'Seymour'
                }
            ]

            for i, answer in enumerate(answers):
                self.assertIn(answer.__dict__, expected_answers)

    def test_deserialise_answers(self):

        serialised_answers = [
            {
                'group_id': 'who-lives-here',
                'group_instance': 0,
                'block_id': 'household-composition',
                'answer_id': 'first-name',
                'answer_instance': 0,
                'value': 'Joe'
            }, {
                'group_id': 'who-lives-here',
                'group_instance': 0,
                'block_id': 'household-composition',
                'answer_id': 'middle-names',
                'answer_instance': 0,
                'value': ''
            }, {
                'group_id': 'who-lives-here',
                'group_instance': 0,
                'block_id': 'household-composition',
                'answer_id': 'last-name',
                'answer_instance': 0,
                'value': 'Bloggs'
            }, {
                'group_id': 'who-lives-here',
                'group_instance': 0,
                'block_id': 'household-composition',
                'answer_id': 'first-name',
                'answer_instance': 1,
                'value': 'Bob'
            }, {
                'group_id': 'who-lives-here',
                'group_instance': 0,
                'block_id': 'household-composition',
                'answer_id': 'middle-names',
                'answer_instance': 1,
                'value': ''
            }, {
                'group_id': 'who-lives-here',
                'group_instance': 0,
                'block_id': 'household-composition',
                'answer_id': 'last-name',
                'answer_instance': 1,
                'value': 'Seymour'
            }
        ]

        expected = {
            'household-0-first-name': 'Joe',
            'household-0-middle-names': '',
            'household-0-last-name': 'Bloggs',
            'household-1-first-name': 'Bob',
            'household-1-middle-names': '',
            'household-1-last-name': 'Seymour',
        }

        self.assertEqual(expected, deserialise_composition_answers(serialised_answers))

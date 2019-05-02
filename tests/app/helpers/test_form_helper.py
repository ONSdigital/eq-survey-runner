from werkzeug.datastructures import MultiDict
from tests.app.app_context_test_case import AppContextTestCase

from app.helpers.form_helper import get_form_for_location, post_form_for_block, get_mapped_answers
from app.questionnaire.location import Location
from app.utilities.schema import load_schema_from_params
from app.data_model.answer_store import AnswerStore
from app.validation.validators import DateRequired, OptionalForm


class TestFormHelper(AppContextTestCase):

    def test_get_form_for_block_location(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_range')

            block_json = schema.get_block('date-block')
            location = Location(block_id='date-block')

            form = get_form_for_location(schema, block_json, location, AnswerStore(), metadata=None)

            self.assertTrue(hasattr(form, 'date-range-from-answer'))
            self.assertTrue(hasattr(form, 'date-range-to-answer'))

            period_from_field = getattr(form, 'date-range-from-answer')
            period_to_field = getattr(form, 'date-range-to-answer')

            self.assertIsInstance(period_from_field.month.validators[0], DateRequired)
            self.assertIsInstance(period_to_field.month.validators[0], DateRequired)

    def test_get_form_and_disable_mandatory_answers(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_range')

            block_json = schema.get_block('date-block')
            location = Location(block_id='date-block')

            form = get_form_for_location(schema, block_json, location,
                                         AnswerStore(), metadata=None, disable_mandatory=True)

            period_from_field = getattr(form, 'date-range-from-answer', None)
            period_to_field = getattr(form, 'date-range-to-answer', None)

            assert period_from_field
            assert period_to_field

            self.assertIsInstance(period_from_field.month.validators[0], OptionalForm)
            self.assertIsInstance(period_to_field.month.validators[0], OptionalForm)


    def test_post_form_for_block_location(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_range')

            block_json = schema.get_block('date-block')

            form = post_form_for_block(schema, block_json, AnswerStore(), metadata=None, request_form={
                'date-range-from-answer-day': '1',
                'date-range-from-answer-month': '05',
                'date-range-from-answer-year': '2015',
                'date-range-to-answer-day': '1',
                'date-range-to-answer-month': '09',
                'date-range-to-answer-year': '2017',
            })

            self.assertTrue(hasattr(form, 'date-range-from-answer'))
            self.assertTrue(hasattr(form, 'date-range-to-answer'))

            period_from_field = getattr(form, 'date-range-from-answer')
            period_to_field = getattr(form, 'date-range-to-answer')

            self.assertIsInstance(period_from_field.month.validators[0], DateRequired)
            self.assertIsInstance(period_to_field.month.validators[0], DateRequired)

            self.assertEqual(period_from_field.data, '2015-05-01')
            self.assertEqual(period_to_field.data, '2017-09-01')

    def test_post_form_and_disable_mandatory(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_range')

            block_json = schema.get_block('date-block')

            form = post_form_for_block(schema, block_json, AnswerStore(), metadata=None, request_form={
            }, disable_mandatory=True)

            self.assertTrue(hasattr(form, 'date-range-from-answer'))
            self.assertTrue(hasattr(form, 'date-range-to-answer'))

            period_from_field = getattr(form, 'date-range-from-answer')
            period_to_field = getattr(form, 'date-range-to-answer')

            self.assertIsInstance(period_from_field.month.validators[0], OptionalForm)
            self.assertIsInstance(period_to_field.month.validators[0], OptionalForm)

    def test_post_form_for_radio_other_not_selected(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'radio_mandatory_with_mandatory_other')

            block_json = schema.get_block('radio-mandatory')

            answer_store = AnswerStore([
                {
                    'answer_id': 'radio-mandatory-answer',
                    'value': 'Other',
                },
                {
                    'answer_id': 'other-answer-mandatory',
                    'value': 'Other text field value',
                }
            ])

            form = post_form_for_block(schema, block_json, answer_store, metadata=None,
                                       request_form=MultiDict({'radio-mandatory-answer': 'Bacon',
                                                               'other-answer-mandatory': 'Old other text'}))

            self.assertTrue(hasattr(form, 'radio-mandatory-answer'))

            other_text_field = getattr(form, 'other-answer-mandatory')
            self.assertEqual(other_text_field.data, '')

    def test_post_form_for_radio_other_selected(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'radio_mandatory_with_mandatory_other')

            block_json = schema.get_block('radio-mandatory')

            answer_store = AnswerStore([
                {
                    'answer_id': 'radio-mandatory-answer',
                    'value': 'Other',
                },
                {
                    'answer_id': 'other-answer-mandatory',
                    'value': 'Other text field value',
                }
            ])

            request_form = MultiDict({
                'radio-mandatory-answer': 'Other',
                'other-answer-mandatory': 'Other text field value',
            })
            form = post_form_for_block(schema, block_json, answer_store, metadata=None, request_form=request_form)

            other_text_field = getattr(form, 'other-answer-mandatory')
            self.assertEqual(other_text_field.data, 'Other text field value')

    def test_get_mapped_answers(self):
        schema = load_schema_from_params('test', 'list_collector')
        location = Location(block_id='add-person', list_name='people')
        answer_store = AnswerStore([
            {
                'answer_id': 'first-name',
                'value': 'Jon',
            },
            {
                'answer_id': 'another-name',
                'value': 'Malcolm',
            },
            {
                'answer_id': 'last-name',
                'value': 'Smith',
            },

        ])

        mapped = get_mapped_answers(schema, answer_store, location)
        self.assertEqual(len(mapped), 2)

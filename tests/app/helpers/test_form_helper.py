import unittest
import uuid

from werkzeug.datastructures import MultiDict
from tests.app.app_context_test_case import AppContextTestCase

from app.helpers.form_helper import get_mapped_answers, get_form_for_location, post_form_for_location
from app.questionnaire.location import Location
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.utilities.schema import load_schema_from_params
from app.data_model.answer_store import AnswerStore, Answer
from app.validation.validators import DateRequired, OptionalForm


class TestFormHelper(AppContextTestCase):

    def test_get_form_for_block_location(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_range')

            block_json = schema.get_block('date-block')
            location = Location(group_id='dates',
                                group_instance=0,
                                block_id='date-block')

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
            location = Location(group_id='dates',
                                group_instance=0,
                                block_id='date-block')

            form = get_form_for_location(schema, block_json, location,
                                         AnswerStore(), metadata=None, disable_mandatory=True)

            self.assertTrue(hasattr(form, 'date-range-from-answer'))
            self.assertTrue(hasattr(form, 'date-range-to-answer'))

            period_from_field = getattr(form, 'date-range-from-answer')
            period_to_field = getattr(form, 'date-range-to-answer')

            self.assertIsInstance(period_from_field.month.validators[0], OptionalForm)
            self.assertIsInstance(period_to_field.month.validators[0], OptionalForm)

    def test_post_form_for_block_location(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_range')

            block_json = schema.get_block('date-block')
            location = Location(group_id='dates',
                                group_instance=0,
                                block_id='date-block')

            form = post_form_for_location(schema, block_json, location, AnswerStore(), metadata=None, request_form={
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
            location = Location(group_id='dates',
                                group_instance=0,
                                block_id='date-block')

            form = post_form_for_location(schema, block_json, location, AnswerStore(), metadata=None, request_form={
            }, disable_mandatory=True)

            self.assertTrue(hasattr(form, 'date-range-from-answer'))
            self.assertTrue(hasattr(form, 'date-range-to-answer'))

            period_from_field = getattr(form, 'date-range-from-answer')
            period_to_field = getattr(form, 'date-range-to-answer')

            self.assertIsInstance(period_from_field.month.validators[0], OptionalForm)
            self.assertIsInstance(period_to_field.month.validators[0], OptionalForm)

    def test_get_form_for_household_composition(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'household_question')

            block_json = schema.get_block('household-composition')
            location = Location('who-lives-here', 0, 'household-composition')
            error_messages = schema.error_messages

            form = get_form_for_location(schema, block_json, location, AnswerStore(), error_messages)

            self.assertTrue(hasattr(form, 'household'))
            self.assertEqual(len(form.household.entries), 1)

            first_field_entry = form.household[0]

            self.assertTrue(hasattr(first_field_entry, 'first-name'))
            self.assertTrue(hasattr(first_field_entry, 'middle-names'))
            self.assertTrue(hasattr(first_field_entry, 'last-name'))

    def test_post_form_for_household_composition(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'household_question')

            block_json = schema.get_block('household-composition')
            location = Location('who-lives-here', 0, 'household-composition')

            form = post_form_for_location(schema, block_json, location, AnswerStore(), metadata=None, request_form={
                'household-0-first-name': 'Joe',
                'household-0-last-name': '',
                'household-1-first-name': 'Bob',
                'household-1-last-name': 'Seymour',
            })

            self.assertEqual(len(form.household.entries), 2)
            self.assertEqual(form.household.entries[0].data, {
                'first-name': 'Joe',
                'middle-names': '',
                'last-name': ''
            })
            self.assertEqual(form.household.entries[1].data, {
                'first-name': 'Bob',
                'middle-names': '',
                'last-name': 'Seymour'
            })

    def test_get_form_for_household_relationship(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'relationship_household')

            block_json = schema.get_block('household-relationships')
            location = Location('who-lives-here-relationship', 0, 'household-relationships')
            error_messages = schema.error_messages

            answer_store = AnswerStore([
                {
                    'group_instance': 0,
                    'group_instance_id': 'who-lives-here-relationship-0',
                    'answer_id': 'first-name',
                    'value': 'Joe',
                    'answer_instance': 0,
                }, {
                    'group_instance': 0,
                    'group_instance_id': 'who-lives-here-relationship-0',
                    'answer_id': 'last-name',
                    'value': 'Bloggs',
                    'answer_instance': 0,
                }, {
                    'group_instance': 0,
                    'group_instance_id': 'who-lives-here-relationship-0',
                    'answer_id': 'first-name',
                    'value': 'Jane',
                    'answer_instance': 1,
                }, {
                    'group_instance': 0,
                    'group_instance_id': 'who-lives-here-relationship-0',
                    'answer_id': 'last-name',
                    'value': 'Bloggs',
                    'answer_instance': 1,
                }
            ])
            form = get_form_for_location(schema, block_json, location, answer_store, error_messages)

            answer = schema.get_answers_for_block('household-relationships')[0]

            self.assertTrue(hasattr(form, answer['id']))

            field_list = getattr(form, answer['id'])

            # With two people, we need to define 1 relationship
            self.assertEqual(len(field_list.entries), 1)

    def test_post_form_for_household_relationship(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'relationship_household')

            block_json = schema.get_block('household-relationships')
            location = Location('who-lives-here-relationship', 0, 'household-relationships')

            answer_store = AnswerStore([
                {
                    'answer_id': 'first-name',
                    'group_instance': 0,
                    'group_instance_id': 'who-lives-here-relationship-0',
                    'value': 'Joe',
                    'answer_instance': 0,
                }, {
                    'answer_id': 'last-name',
                    'group_instance': 0,
                    'group_instance_id': 'who-lives-here-relationship-0',
                    'value': 'Bloggs',
                    'answer_instance': 0,
                }, {
                    'answer_id': 'first-name',
                    'group_instance': 0,
                    'group_instance_id': 'who-lives-here-relationship-0',
                    'value': 'Jane',
                    'answer_instance': 1,
                }, {
                    'answer_id': 'last-name',
                    'group_instance': 0,
                    'group_instance_id': 'who-lives-here-relationship-0',
                    'value': 'Bloggs',
                    'answer_instance': 1,
                }
            ])

            answer = schema.get_answers_for_block('household-relationships')[0]

            form = post_form_for_location(schema, block_json, location, answer_store, metadata=None,
                                          request_form=MultiDict({'{answer_id}-0'.format(answer_id=answer['id']): '3'}))

            self.assertTrue(hasattr(form, answer['id']))

            field_list = getattr(form, answer['id'])

            # With two people, we need to define 1 relationship
            self.assertEqual(len(field_list.entries), 1)

            # Check the data matches what was passed from request
            self.assertEqual(field_list.entries[0].data, '3')

    def test_get_form_for_household_relationship_driven_by_multiple_answers(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'routing_on_answer_from_driving_repeating_group')

            block_json = schema.get_block('relationships')
            location = Location('household-relationships', 0, 'relationships')
            error_messages = schema.error_messages

            primary_group_instance_id = str(uuid.uuid4())
            repeating_group_1_instance_id = str(uuid.uuid4())
            repeating_group_2_instance_id = str(uuid.uuid4())

            answer_store = AnswerStore({})
            answer_store.add_or_update(Answer(
                answer_id='primary-name',
                value='Jon',
                group_instance=0,
                group_instance_id=primary_group_instance_id
            ))
            answer_store.add_or_update(Answer(
                answer_id='primary-live-here',
                value='No',
                group_instance=0,
                group_instance_id=primary_group_instance_id
            ))
            answer_store.add_or_update(Answer(
                answer_id='repeating-anyone-else',
                answer_instance=0,
                value='Yes',
                group_instance=0,
            ))
            answer_store.add_or_update(Answer(
                answer_id='repeating-name',
                answer_instance=0,
                value='Adam',
                group_instance=0,
                group_instance_id=repeating_group_1_instance_id
            ))
            answer_store.add_or_update(Answer(
                answer_id='repeating-anyone-else',
                answer_instance=0,
                value='Yes',
                group_instance=1,
            ))
            answer_store.add_or_update(Answer(
                answer_id='repeating-name',
                answer_instance=0,
                value='Ben',
                group_instance=1,
                group_instance_id=repeating_group_2_instance_id
            ))
            answer_store.add_or_update(Answer(
                answer_id='repeating-anyone-else',
                answer_instance=0,
                value='No',
                group_instance=2,
            ))

            form = get_form_for_location(schema, block_json, location, answer_store, error_messages)

            answer = schema.get_answers_for_block('relationships')[0]

            self.assertTrue(hasattr(form, answer['id']))

            field_list = getattr(form, answer['id'])

            # With three people, we need to define 2 relationships
            self.assertEqual(len(field_list.entries), 2)

    def test_post_form_for_household_relationship_driven_by_multiple_answers(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'routing_on_answer_from_driving_repeating_group')

            block_json = schema.get_block('relationships')
            location = Location('household-relationships', 0, 'relationships')

            primary_group_instance_id = str(uuid.uuid4())
            repeating_group_1_instance_id = str(uuid.uuid4())
            repeating_group_2_instance_id = str(uuid.uuid4())

            answer_store = AnswerStore({})
            answer_store.add_or_update(Answer(
                answer_id='primary-name',
                value='Jon',
                group_instance=0,
                group_instance_id=primary_group_instance_id
            ))
            answer_store.add_or_update(Answer(
                answer_id='primary-live-here',
                value='No',
                group_instance=0,
                group_instance_id=primary_group_instance_id
            ))
            answer_store.add_or_update(Answer(
                answer_id='repeating-anyone-else',
                answer_instance=0,
                value='Yes',
                group_instance=0,
            ))
            answer_store.add_or_update(Answer(
                answer_id='repeating-name',
                answer_instance=0,
                value='Adam',
                group_instance=0,
                group_instance_id=repeating_group_1_instance_id
            ))
            answer_store.add_or_update(Answer(
                answer_id='repeating-anyone-else',
                answer_instance=0,
                value='Yes',
                group_instance=1,
            ))
            answer_store.add_or_update(Answer(
                answer_id='repeating-name',
                answer_instance=0,
                value='Ben',
                group_instance=1,
                group_instance_id=repeating_group_2_instance_id
            ))
            answer_store.add_or_update(Answer(
                answer_id='repeating-anyone-else',
                answer_instance=0,
                value='No',
                group_instance=2,
            ))

            answer = schema.get_answers_for_block('relationships')[0]

            form = post_form_for_location(schema, block_json, location, answer_store, metadata=None,
                                          request_form=MultiDict({'{answer_id}-0'.format(answer_id=answer['id']): '3'}))

            self.assertTrue(hasattr(form, answer['id']))

            field_list = getattr(form, answer['id'])

            # With three people, we need to define 2 relationships
            self.assertEqual(len(field_list.entries), 2)

            # Check the data matches what was passed from request
            self.assertEqual(field_list.entries[0].data, '3')

    def test_post_form_for_radio_other_not_selected(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'radio_mandatory_with_mandatory_other')

            block_json = schema.get_block('radio-mandatory')
            location = Location('radio', 0, 'radio-mandatory')

            answer_store = AnswerStore([
                {
                    'answer_id': 'radio-mandatory-answer',
                    'block_id': 'radio-mandatory',
                    'value': 'Other',
                    'answer_instance': 0,
                },
                {
                    'answer_id': 'other-answer-mandatory',
                    'block_id': 'radio-mandatory',
                    'value': 'Other text field value',
                    'answer_instance': 0,
                }
            ])

            form = post_form_for_location(schema, block_json, location, answer_store, metadata=None,
                                          request_form=MultiDict({'radio-mandatory-answer': 'Bacon',
                                                                  'other-answer-mandatory': 'Old other text'}))

            self.assertTrue(hasattr(form, 'radio-mandatory-answer'))

            other_text_field = getattr(form, 'other-answer-mandatory')
            self.assertEqual(other_text_field.data, '')

    def test_post_form_for_radio_other_selected(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'radio_mandatory_with_mandatory_other')

            block_json = schema.get_block('radio-mandatory')
            location = Location('radio', 0, 'radio-mandatory')

            answer_store = AnswerStore([
                {
                    'answer_id': 'radio-mandatory-answer',
                    'block_id': 'radio-mandatory',
                    'value': 'Other',
                    'answer_instance': 0,
                },
                {
                    'answer_id': 'other-answer-mandatory',
                    'block_id': 'radio-mandatory',
                    'value': 'Other text field value',
                    'answer_instance': 0,
                }
            ])

            request_form = MultiDict({
                'radio-mandatory-answer': 'Other',
                'other-answer-mandatory': 'Other text field value',
            })
            form = post_form_for_location(schema, block_json, location, answer_store, metadata=None, request_form=request_form)

            other_text_field = getattr(form, 'other-answer-mandatory')
            self.assertEqual(other_text_field.data, 'Other text field value')


class TestGetMappedAnswers(unittest.TestCase):

    def setUp(self):
        self.store = AnswerStore(None)

    def tearDown(self):
        self.store.clear()

    def test_maps_and_filters_answers(self):
        questionnaire = {
            'sections': [{
                'id': 'section1',
                'groups': [
                    {
                        'id': 'group1',
                        'blocks': [
                            {
                                'id': 'block1',
                                'questions': [{
                                    'id': 'question1',
                                    'answers': [
                                        {
                                            'id': 'answer1',
                                            'type': 'TextArea'
                                        }
                                    ]
                                }]
                            },
                            {
                                'id': 'block2',
                                'questions': [{
                                    'id': 'question2',
                                    'answers': [
                                        {
                                            'id': 'answer2',
                                            'type': 'TextArea'
                                        }
                                    ]
                                }]
                            }]
                    }]
            }]
        }
        schema = QuestionnaireSchema(questionnaire)

        answer_1 = Answer(
            answer_id='answer2',
            answer_instance=1,
            group_instance_id='group-1',
            group_instance=1,
            value=25,
        )
        answer_2 = Answer(
            answer_id='answer1',
            answer_instance=1,
            group_instance_id='group-1',
            group_instance=1,
            value=65,
        )

        self.store.add_or_update(answer_1)
        self.store.add_or_update(answer_2)

        expected_answers = {
            'answer1_1': 65
        }

        self.assertEqual(get_mapped_answers(schema, self.store, block_id='block1', group_instance=1, group_instance_id='group-1'), expected_answers)

    def test_returns_ordered_map(self):

        questionnaire = {
            'sections': [{
                'id': 'section1',
                'groups': [{
                    'id': 'group1',
                    'blocks': [{
                        'id': 'block1',
                        'questions': [{
                            'id': 'question1',
                            'answers': [
                                {
                                    'id': 'answer1',
                                    'type': 'TextArea'
                                }
                            ]
                        }]
                    }]
                }]
            }]
        }
        schema = QuestionnaireSchema(questionnaire)

        answer = Answer(
            answer_id='answer1',
            group_instance_id='group-1',
            group_instance=1,
            value=25,
        )

        for i in range(0, 100):
            answer.answer_instance = i

            self.store.add_or_update(answer)

        last_instance = -1

        self.assertEqual(len(self.store), 100)

        mapped = get_mapped_answers(schema, self.store, block_id='block1', group_instance=1, group_instance_id='group-1')

        for key, _ in mapped.items():
            pos = key.find('_')

            instance = 0 if pos == -1 else int(key[pos + 1:])

            self.assertGreater(instance, last_instance)

            last_instance = instance

from unittest.mock import MagicMock

from app.data_model.answer_store import AnswerStore, Answer
from app.questionnaire.completeness import Completeness
from app.questionnaire.location import Location
from app.questionnaire.navigation import Navigation
from app.utilities.schema import load_schema_from_params

from tests.app.app_context_test_case import AppContextTestCase


# pylint: disable=R0904,C0302
class TestNavigation(AppContextTestCase):

    def test_navigation_no_blocks_completed(self):
        schema = load_schema_from_params('test', 'navigation')
        schema.answer_is_in_repeating_group = MagicMock(return_value=False)
        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        navigation = _create_navigation(schema, AnswerStore(), metadata, [], [])

        user_navigation = [
            {
                'link_name': 'Property Details',
                'highlight': True,
                'repeating': False,
                'completed': False,
                'link_url': Location('property-details', 0, 'insurance-type').url(metadata)
            },
            {
                'link_name': 'Household Composition',
                'highlight': False,
                'repeating': False,
                'completed': False,
                'link_url': Location('multiple-questions-group', 0, 'household-composition').url(metadata)
            },
            {
                'link_name': 'Extra Cover',
                'highlight': False,
                'repeating': False,
                'completed': False,
                'link_url': Location('extra-cover', 0, 'extra-cover-block').url(metadata)
            },
            {
                'link_name': 'Payment Details',
                'highlight': False,
                'repeating': False,
                'completed': False,
                'link_url': Location('skip-payment-group', 0, 'skip-payment').url(metadata)
            }
        ]
        self.assertEqual(navigation.build_navigation('property-details', 0), user_navigation)

    def test_non_repeating_block_completed(self):
        schema = load_schema_from_params('test', 'navigation')
        schema.answer_is_in_repeating_group = MagicMock(return_value=True)

        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        answer_store = AnswerStore()

        answer_1 = Answer(
            value='Contents',
            group_instance=0,
            answer_instance=0,
            answer_id='insurance-type-answer'
        )

        answer_store.add(answer_1)

        completed_blocks = [
            Location('property-details', 0, 'insurance-type'),
            Location('property-details', 0, 'insurance-address')
        ]

        routing_path = [
            Location('property-details', 0, 'insurance-type'),
            Location('skip-payment-group', 0, 'skip-payment'),
        ]

        navigation = _create_navigation(schema, answer_store, metadata, completed_blocks, routing_path)

        user_navigation = [
            {
                'link_name': 'Property Details',
                'highlight': True,
                'repeating': False,
                'completed': True,
                'link_url': Location('property-details', 0, 'insurance-type').url(metadata)
            },
            {
                'link_name': 'Property Interstitial',
                'highlight': False,
                'repeating': False,
                'completed': False,
                'link_url': Location('property-interstitial-group', 0, 'property-interstitial').url(metadata)
            },
            {
                'link_name': 'Household Composition',
                'highlight': False,
                'repeating': False,
                'completed': False,
                'link_url': Location('multiple-questions-group', 0, 'household-composition').url(metadata)
            },
            {
                'link_name': 'Extra Cover',
                'highlight': False,
                'repeating': False,
                'completed': False,
                'link_url': Location('extra-cover', 0, 'extra-cover-block').url(metadata)
            },
            {
                'link_name': 'Payment Details',
                'highlight': False,
                'repeating': False,
                'completed': False,
                'link_url': Location('skip-payment-group', 0, 'skip-payment').url(metadata)
            }

        ]
        self.assertEqual(navigation.build_navigation('property-details', 0), user_navigation)

    def test_navigation_repeating_household_and_hidden_household_groups_completed(self):
        schema = load_schema_from_params('test', 'navigation')
        schema.answer_is_in_repeating_group = MagicMock(return_value=True)

        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        completed_blocks = [
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('repeating-group', 0, 'repeating-block-1'),
            Location('repeating-group', 0, 'repeating-block-2'),
            Location('repeating-group', 1, 'repeating-block-1'),
            Location('repeating-group', 1, 'repeating-block-2')
        ]

        routing_path = [
            Location('property-details', 0, 'insurance-type'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('repeating-group', 0, 'repeating-block-1'),
            Location('repeating-group', 0, 'repeating-block-2'),
            Location('repeating-group', 1, 'repeating-block-1'),
            Location('repeating-group', 1, 'repeating-block-2'),
            Location('skip-payment-group', 0, 'skip-payment')
        ]

        navigation = _create_navigation(schema, AnswerStore(), metadata, completed_blocks, routing_path)

        navigation.answer_store.answers = [
            {
                'group_instance': 0,
                'answer_instance': 0,
                'answer_id': 'first-name',
                'value': 'Jim',
            },
            {
                'group_instance': 0,
                'answer_instance': 1,
                'answer_id': 'first-name',
                'value': 'Ben',
            },
            {
                'group_instance': 0,
                'answer_instance': 0,
                'answer_id': 'what-is-your-age',
                'value': None,
            },
            {
                'group_instance': 0,
                'answer_instance': 0,
                'answer_id': 'what-is-your-shoe-size',
                'value': None,
            },
            {
                'group_instance': 1,
                'answer_instance': 0,
                'answer_id': 'what-is-your-age',
                'value': None,
            },
            {
                'group_instance': 1,
                'answer_instance': 0,
                'answer_id': 'what-is-your-shoe-size',
                'value': None,
            }
        ]

        user_navigation = [
            {
                'link_name': 'Property Details',
                'repeating': False,
                'completed': False,
                'highlight': True,
                'link_url': Location('property-details', 0, 'insurance-type').url(metadata)
            },
            {
                'link_name': 'Household Composition',
                'highlight': False,
                'repeating': False,
                'completed': True,
                'link_url': Location('multiple-questions-group', 0, 'household-composition').url(metadata)
            },
            {
                'link_name': 'Jim',
                'repeating': True,
                'completed': True,
                'highlight': False,
                'link_url': Location('repeating-group', 0, 'repeating-block-1').url(metadata)
            },
            {
                'link_name': 'Ben',
                'repeating': True,
                'completed': True,
                'highlight': False,
                'link_url': Location('repeating-group', 1, 'repeating-block-1').url(metadata)
            },
            {
                'link_name': 'Extra Cover',
                'repeating': False,
                'completed': False,
                'highlight': False,
                'link_url': Location('extra-cover', 0, 'extra-cover-block').url(metadata)
            },
            {
                'link_name': 'Payment Details',
                'repeating': False,
                'completed': False,
                'highlight': False,
                'link_url': Location('skip-payment-group', 0, 'skip-payment').url(metadata)
            }
        ]
        self.assertEqual(navigation.build_navigation('property-details', 0), user_navigation)

    def test_navigation_repeating_group_extra_answered_not_completed(self):
        schema = load_schema_from_params('test', 'navigation')
        schema.answer_is_in_repeating_group = MagicMock(return_value=True)

        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        completed_blocks = [
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('extra-cover', 0, 'extra-cover-block')
        ]

        answer_store = AnswerStore()

        answer_1 = Answer(
            answer_instance=0,
            answer_id='first-name',
            group_instance=0,
            value='Person1'
        )
        answer_2 = Answer(
            answer_instance=1,
            answer_id='first-name',
            group_instance=0,
            value='Person2'
        )
        answer_3 = Answer(
            answer_instance=1,
            answer_id='extra-cover-answer',
            group_instance=0,
            value=2
        )

        answer_store.add(answer_1)
        answer_store.add(answer_2)
        answer_store.add(answer_3)

        routing_path = [
            Location('property-details', 0, 'insurance-type'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('extra-cover', 0, 'extra-cover-block'),
            Location('extra-cover-items-group', 0, 'extra-cover-items'),
            Location('skip-payment-group', 0, 'skip-payment'),
        ]

        navigation = _create_navigation(schema, answer_store, metadata, completed_blocks, routing_path)

        user_navigation = [
            {
                'completed': False,
                'highlight': True,
                'repeating': False,
                'link_name': 'Property Details',
                'link_url': Location('property-details', 0, 'insurance-type').url(metadata)
            },
            {
                'link_name': 'Household Composition',
                'highlight': False,
                'repeating': False,
                'completed': True,
                'link_url': Location('multiple-questions-group', 0, 'household-composition').url(metadata)
            },
            {
                'completed': False,
                'highlight': False,
                'repeating': True,
                'link_name': 'Person1',
                'link_url': Location('repeating-group', 0, 'repeating-block-1').url(metadata),
            },
            {
                'completed': False,
                'highlight': False,
                'repeating': True,
                'link_name': 'Person2',
                'link_url': Location('repeating-group', 1, 'repeating-block-1').url(metadata),
            },
            {
                'completed': True,
                'highlight': False,
                'repeating': False,
                'link_name': 'Extra Cover',
                'link_url': Location('extra-cover', 0, 'extra-cover-block').url(metadata),
            },
            {
                'completed': False,
                'highlight': False,
                'repeating': False,
                'link_name': 'Extra Cover Items',
                'link_url': Location('extra-cover-items-group', 0, 'extra-cover-items').url(metadata)
            },
            {
                'completed': False,
                'highlight': False,
                'repeating': False,
                'link_name': 'Payment Details',
                'link_url': Location('skip-payment-group', 0, 'skip-payment').url(metadata),
            }
        ]

        self.assertEqual(navigation.build_navigation('property-details', 0), user_navigation)

    def test_navigation_repeating_group_extra_answered_completed(self):
        schema = load_schema_from_params('test', 'navigation')
        schema.answer_is_in_repeating_group = MagicMock(return_value=True)

        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        completed_blocks = [
            Location('extra-cover', 0, 'extra-cover-block'),
            Location('extra-cover-items-group', 0, 'extra-cover-items'),
            Location('extra-cover-items-group', 0, 'extra-cover-items-radio'),
            Location('extra-cover-items-group', 1, 'extra-cover-items'),
            Location('extra-cover-items-group', 1, 'extra-cover-items-radio'),
        ]

        answer_store = AnswerStore()

        answer_1 = Answer(
            value=2,
            group_instance=0,
            answer_id='extra-cover-answer',
            answer_instance=0

        )
        answer_2 = Answer(
            value='1',
            group_instance=0,
            answer_id='extra-cover-items-answer',
            answer_instance=0
        )
        answer_3 = Answer(
            value='Yes',
            group_instance=0,
            answer_id='extra-cover-items-radio-answer',
            answer_instance=0
        )
        answer_4 = Answer(
            value='2',
            group_instance=1,
            answer_id='extra-cover-items-answer',
            answer_instance=0
        )
        answer_5 = Answer(
            value='Yes',
            group_instance=1,
            answer_id='extra-cover-items-radio-answer',
            answer_instance=0
        )

        answer_store.add(answer_1)
        answer_store.add(answer_2)
        answer_store.add(answer_3)
        answer_store.add(answer_4)
        answer_store.add(answer_5)

        routing_path = [
            Location('property-details', 0, 'insurance-type'),
            Location('extra-cover', 0, 'extra-cover-block'),
            Location('extra-cover-items-group', 0, 'extra-cover-items'),
            Location('extra-cover-items-group', 0, 'extra-cover-items-radio'),
            Location('extra-cover-items-group', 1, 'extra-cover-items'),
            Location('extra-cover-items-group', 1, 'extra-cover-items-radio'),
            Location('skip-payment-group', 0, 'skip-payment'),
        ]

        navigation = _create_navigation(schema, answer_store, metadata, completed_blocks, routing_path)

        user_navigation = [
            {
                'repeating': False,
                'highlight': True,
                'completed': False,
                'link_name': 'Property Details',
                'link_url': Location('property-details', 0, 'insurance-type').url(metadata)
            },
            {
                'link_name': 'Household Composition',
                'highlight': False,
                'repeating': False,
                'completed': False,
                'link_url': Location('multiple-questions-group', 0, 'household-composition').url(metadata)
            },
            {
                'repeating': False,
                'highlight': False,
                'completed': True,
                'link_name': 'Extra Cover',
                'link_url': Location('extra-cover', 0, 'extra-cover-block').url(metadata)
            },
            {
                'repeating': False,
                'highlight': False,
                'completed': True,
                'link_name': 'Extra Cover Items',
                'link_url': Location('extra-cover-items-group', 0, 'extra-cover-items').url(metadata)
            },
            {
                'repeating': False,
                'highlight': False,
                'completed': False,
                'link_name': 'Payment Details',
                'link_url': Location('skip-payment-group', 0, 'skip-payment').url(metadata)
            }
        ]

        self.assertEqual(navigation.build_navigation('property-details', 0), user_navigation)

    def test_navigation_repeating_group_link_name_format(self):
        schema = load_schema_from_params('test', 'navigation')
        schema.answer_is_in_repeating_group = MagicMock(return_value=True)

        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        completed_blocks = [
            Location('multiple-questions-group', 0, 'household-composition'),
        ]

        answer_store = AnswerStore()

        answer_1 = Answer(
            answer_instance=0,
            answer_id='first-name',
            group_instance=0,
            value='Joe'
        )
        answer_2 = Answer(
            answer_instance=0,
            answer_id='last-name',
            group_instance=0,
            value='Bloggs'
        )
        answer_3 = Answer(
            answer_instance=1,
            answer_id='first-name',
            group_instance=0,
            value='Jane'
        )
        answer_4 = Answer(
            answer_instance=1,
            answer_id='last-name',
            group_instance=0,
            value='Doe'
        )

        answer_store.add(answer_1)
        answer_store.add(answer_2)
        answer_store.add(answer_3)
        answer_store.add(answer_4)

        routing_path = [
            Location('property-details', 0, 'insurance-type'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('skip-payment-group', 0, 'skip-payment'),
        ]

        navigation = _create_navigation(schema, answer_store, metadata, completed_blocks, routing_path)

        user_navigation = [
            {
                'link_name': 'Property Details',
                'highlight': True,
                'repeating': False,
                'completed': False,
                'link_url': Location('property-details', 0, 'insurance-type').url(metadata)
            },
            {
                'repeating': False,
                'completed': True,
                'highlight': False,
                'link_name': 'Household Composition',
                'link_url': Location('multiple-questions-group', 0, 'household-composition').url(metadata)
            },
            {
                'repeating': True,
                'link_name': 'Joe Bloggs',
                'completed': False,
                'highlight': False,
                'link_url': Location('repeating-group', 0, 'repeating-block-1').url(metadata)
            },
            {
                'repeating': True,
                'link_name': 'Jane Doe',
                'completed': False,
                'highlight': False,
                'link_url': Location('repeating-group', 1, 'repeating-block-1').url(metadata)
            },
            {
                'link_name': 'Extra Cover',
                'highlight': False,
                'repeating': False,
                'completed': False,
                'link_url': Location('extra-cover', 0, 'extra-cover-block').url(metadata)
            },
            {
                'link_name': 'Payment Details',
                'highlight': False,
                'repeating': False,
                'completed': False,
                'link_url': Location('skip-payment-group', 0, 'skip-payment').url(metadata)
            }
        ]

        self.assertEqual(navigation.build_navigation('property-details', 0), user_navigation)

    def test_navigation_skip_condition_hide_group(self):
        schema = load_schema_from_params('test', 'navigation')
        schema.answer_is_in_repeating_group = MagicMock(return_value=True)

        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        completed_blocks = []

        answer_store = AnswerStore()

        answer_1 = Answer(
            value='Buildings',
            group_instance=0,
            answer_instance=0,
            answer_id='insurance-type-answer'
        )

        answer_store.add(answer_1)
        navigation = _create_navigation(schema, answer_store, metadata, completed_blocks, [])
        user_navigation = navigation.build_navigation('property-details', 0)
        link_names = [d['link_name'] for d in user_navigation]
        self.assertNotIn('Property Interstitial', link_names)

    def test_navigation_skip_condition_show_group(self):
        schema = load_schema_from_params('test', 'navigation')
        schema.answer_is_in_repeating_group = MagicMock(return_value=True)

        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        completed_blocks = []

        answer_store = AnswerStore()

        answer_1 = Answer(
            value='Contents',
            group_instance=0,
            answer_instance=0,
            answer_id='insurance-type-answer'
        )

        answer_store.add(answer_1)

        navigation = _create_navigation(schema, answer_store, metadata, completed_blocks, [])

        user_navigation = navigation.build_navigation('property-details', 0)
        link_names = [d['link_name'] for d in user_navigation]
        self.assertIn('Property Interstitial', link_names)

    def test_navigation_skip_condition_change_answer(self):
        schema = load_schema_from_params('test', 'navigation')
        schema.answer_is_in_repeating_group = MagicMock(return_value=True)

        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        completed_blocks = []

        answer_store = AnswerStore()

        answer_1 = Answer(
            value='Contents',
            group_instance=0,
            answer_instance=0,
            answer_id='insurance-type-answer'
        )

        answer_store.add(answer_1)
        navigation = _create_navigation(schema, answer_store, metadata, completed_blocks, [])

        user_navigation = navigation.build_navigation('property-details', 0)
        link_names = [d['link_name'] for d in user_navigation]
        self.assertIn('Property Interstitial', link_names)

        change_answer = Answer(
            value='Buildings',
            group_instance=0,
            answer_instance=0,
            answer_id='insurance-type-answer'
        )

        answer_store.update(change_answer)

        navigation = _create_navigation(schema, answer_store, metadata, completed_blocks, [])
        user_navigation = navigation.build_navigation('property-details', 0)

        link_names = [d['link_name'] for d in user_navigation]
        self.assertNotIn('Property Interstitial', link_names)

    def test_build_navigation_returns_none_when_schema_navigation_is_false(self):
        # Given
        schema = load_schema_from_params('test', 'navigation')
        schema.json['navigation'] = {'visible': False}
        completed_blocks = []
        metadata = {}
        navigation = _create_navigation(schema, AnswerStore(), metadata, completed_blocks, [])

        # When
        nav_menu = navigation.build_navigation('group-1', 'group-instance-1')

        # Then
        self.assertIsNone(nav_menu)

    def test_build_navigation_returns_none_when_no_schema_navigation_property(self):
        # Given
        schema = load_schema_from_params('test', 'navigation')
        del schema.json['navigation']
        completed_blocks = []
        metadata = {}
        navigation = _create_navigation(schema, AnswerStore(), metadata, completed_blocks, [])

        # When
        nav_menu = navigation.build_navigation('group-1', 'group-instance-1')

        # Then
        self.assertIsNone(nav_menu)

    def test_build_navigation_returns_navigation_when_schema_navigation_is_true(self):
        # Given
        schema = load_schema_from_params('test', 'navigation')
        schema.answer_is_in_repeating_group = MagicMock(return_value=True)
        schema.json['navigation'] = {'visible': True}

        completed_blocks = []
        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }
        navigation = _create_navigation(schema, AnswerStore(), metadata, completed_blocks, [])

        # When
        nav_menu = navigation.build_navigation('group-1', 'group-instance-1')

        # Then
        self.assertIsNotNone(nav_menu)

    def test_build_navigation_summary_link_hidden_when_no_sections_completed(self):
        schema = load_schema_from_params('test', 'navigation')
        schema.answer_is_in_repeating_group = MagicMock(return_value=True)

        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        navigation = _create_navigation(schema, AnswerStore(), metadata, [], [])

        confirmation_link = {
            'link_name': 'Summary',
            'highlight': False,
            'repeating': False,
            'completed': False,
            'link_url': Location('summary-group', 0, 'summary').url(metadata)
        }

        self.assertNotIn(confirmation_link, navigation.build_navigation('property-details', 0))

    def test_build_navigation_summary_link_hidden_when_not_all_sections_completed(self):
        schema = load_schema_from_params('test', 'navigation')
        schema.answer_is_in_repeating_group = MagicMock(return_value=True)

        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        completed_blocks = [
            Location('property-details', 0, 'insurance-type'),
            Location('property-details', 0, 'insurance-address'),
            Location('property-details', 0, 'property-interstitial'),
            Location('house-details', 0, 'house-type'),
            Location('multiple-questions-group', 0, 'household-composition'),
        ]

        navigation = _create_navigation(schema, AnswerStore(), metadata, completed_blocks, [])

        confirmation_link = {
            'link_name': 'Summary',
            'highlight': False,
            'repeating': False,
            'completed': False,
            'link_url': Location('summary-group', 0, 'summary').url(metadata)
        }

        navigation_links = navigation.build_navigation('property-details', 0)
        self.assertNotIn(confirmation_link, navigation_links)
        self.assertEqual(len(navigation_links), 4)

    def test_build_navigation_summary_link_visible_when_all_sections_complete(self):
        schema = load_schema_from_params('test', 'navigation')
        schema.answer_is_in_repeating_group = MagicMock(return_value=True)

        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        completed_blocks = [
            Location('property-details', 0, 'insurance-type'),
            Location('property-details', 0, 'insurance-address'),
            Location('property-details', 0, 'property-interstitial'),
            Location('house-details', 0, 'house-type'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('repeating-group', 0, 'repeating-block-1'),
            Location('repeating-group', 0, 'repeating-block-2'),
            Location('extra-cover', 0, 'extra-cover-block'),
            Location('extra-cover', 0, 'extra-cover-interstitial'),
            Location('payment-details', 0, 'credit-card'),
            Location('payment-details', 0, 'expiry-date'),
            Location('payment-details', 0, 'security-code'),
            Location('payment-details', 0, 'security-code-interstitial'),
            Location('extra-cover-items-group', 0, 'extra-cover-items'),
            Location('extra-cover-items-group', 0, 'extra-cover-items-radio'),
            Location('skip-payment-group', 0, 'skip-payment'),
        ]

        routing_path = [
            Location('property-details', 0, 'insurance-type'),
            Location('property-details', 0, 'insurance-address'),
            Location('property-details', 0, 'property-interstitial'),
            Location('house-details', 0, 'house-type'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('repeating-group', 0, 'repeating-block-1'),
            Location('repeating-group', 0, 'repeating-block-2'),
            Location('payment-details', 0, 'credit-card'),
            Location('payment-details', 0, 'expiry-date'),
            Location('payment-details', 0, 'security-code'),
            Location('payment-details', 0, 'security-code-interstitial'),
            Location('extra-cover', 0, 'extra-cover-block'),
            Location('extra-cover', 0, 'extra-cover-interstitial'),
            Location('extra-cover-items-group', 0, 'extra-cover-items'),
            Location('extra-cover-items-group', 0, 'extra-cover-items-radio'),
            Location('skip-payment-group', 0, 'skip-payment'),
            Location('summary-group', 0, 'summary'),
        ]

        navigation = _create_navigation(schema, AnswerStore(), metadata, completed_blocks, routing_path)

        confirmation_link = {
            'link_name': 'Summary',
            'highlight': False,
            'repeating': False,
            'completed': False,
            'link_url': Location('summary-group', 0, 'summary').url(metadata)
        }

        navigation_links = navigation.build_navigation('property-details', 0)
        self.assertIn(confirmation_link, navigation_links)
        self.assertEqual(len(navigation_links), 5)

    def test_build_navigation_submit_answers_link_not_visible_for_survey_with_summary(self):
        schema = load_schema_from_params('test', 'navigation')
        schema.answer_is_in_repeating_group = MagicMock(return_value=True)

        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        completed_blocks = [
            Location('property-details', 0, 'insurance-type'),
            Location('property-details', 0, 'insurance-address'),
            Location('property-details', 0, 'property-interstitial'),
            Location('house-details', 0, 'house-type'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('repeating-group', 0, 'repeating-block-1'),
            Location('repeating-group', 0, 'repeating-block-2'),
            Location('extra-cover', 0, 'extra-cover-block'),
            Location('extra-cover', 0, 'extra-cover-interstitial'),
            Location('payment-details', 0, 'credit-card'),
            Location('payment-details', 0, 'expiry-date'),
            Location('payment-details', 0, 'security-code'),
            Location('payment-details', 0, 'security-code-interstitial'),
            Location('extra-cover-items-group', 0, 'extra-cover-items'),
        ]

        navigation = _create_navigation(schema, AnswerStore(), metadata, completed_blocks, [])

        confirmation_link = {
            'link_name': 'Submit answers',
            'highlight': False,
            'repeating': False,
            'completed': False,
            'link_url': Location('confirmation-group', 0, 'confirmation').url(metadata)
        }

        navigation_links = navigation.build_navigation('property-details', 0)
        self.assertNotIn(confirmation_link, navigation_links)
        self.assertEqual(len(navigation_links), 4)

    def test_build_navigation_submit_answers_link_hidden_when_no_sections_completed(self):
        schema = load_schema_from_params('test', 'navigation_confirmation')
        schema.answer_is_in_repeating_group = MagicMock(return_value=True)

        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        navigation = _create_navigation(schema, AnswerStore(), metadata, [], [])

        confirmation_link = {
            'link_name': 'Submit answers',
            'highlight': False,
            'repeating': False,
            'completed': False,
            'link_url': Location('confirmation-group', 0, 'confirmation').url(metadata)
        }

        navigation_links = navigation.build_navigation('property-details', 0)

        self.assertNotIn(confirmation_link, navigation_links)
        self.assertEqual(len(navigation_links), 4)

    def test_build_navigation_submit_answers_link_hidden_when_not_all_sections_completed(self):
        schema = load_schema_from_params('test', 'navigation_confirmation')
        schema.answer_is_in_repeating_group = MagicMock(return_value=True)

        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        completed_blocks = [
            Location('property-details', 0, 'insurance-type'),
            Location('property-details', 0, 'insurance-address'),
            Location('property-details', 0, 'property-interstitial'),
            Location('house-details', 0, 'house-type'),
            Location('multiple-questions-group', 0, 'household-composition'),
        ]

        navigation = _create_navigation(schema, AnswerStore(), metadata, completed_blocks, [])

        confirmation_link = {
            'link_name': 'Submit answers',
            'highlight': False,
            'repeating': False,
            'completed': False,
            'link_url': Location('confirmation-group', 0, 'confirmation').url(metadata)
        }

        navigation_links = navigation.build_navigation('property-details', 0)
        self.assertNotIn(confirmation_link, navigation_links)
        self.assertEqual(len(navigation_links), 4)

    def test_build_navigation_submit_answers_link_visible_when_all_sections_complete(self):
        schema = load_schema_from_params('test', 'navigation_confirmation')
        schema.answer_is_in_repeating_group = MagicMock(return_value=True)

        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        completed_blocks = [
            Location('property-details', 0, 'insurance-type'),
            Location('property-details', 0, 'insurance-address'),
            Location('property-details', 0, 'property-interstitial'),
            Location('house-details', 0, 'house-type'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('repeating-group', 0, 'repeating-block-1'),
            Location('repeating-group', 0, 'repeating-block-2'),
            Location('extra-cover', 0, 'extra-cover-block'),
            Location('extra-cover', 0, 'extra-cover-interstitial'),
            Location('payment-details', 0, 'credit-card'),
            Location('payment-details', 0, 'expiry-date'),
            Location('payment-details', 0, 'security-code'),
            Location('payment-details', 0, 'security-code-interstitial'),
            Location('extra-cover-items-group', 0, 'extra-cover-items'),
        ]

        routing_path = [
            Location('property-details', 0, 'insurance-type'),
            Location('property-details', 0, 'insurance-address'),
            Location('property-details', 0, 'property-interstitial'),
            Location('house-details', 0, 'house-type'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('repeating-group', 0, 'repeating-block-1'),
            Location('repeating-group', 0, 'repeating-block-2'),
            Location('extra-cover', 0, 'extra-cover-block'),
            Location('extra-cover', 0, 'extra-cover-interstitial'),
            Location('payment-details', 0, 'credit-card'),
            Location('payment-details', 0, 'expiry-date'),
            Location('payment-details', 0, 'security-code'),
            Location('payment-details', 0, 'security-code-interstitial'),
            Location('extra-cover-items-group', 0, 'extra-cover-items'),
            Location('confirmation-group', 0, 'confirmation'),
        ]

        navigation = _create_navigation(schema, AnswerStore(), metadata, completed_blocks, routing_path)

        confirmation_link = {
            'link_name': 'Submit answers',
            'highlight': False,
            'repeating': False,
            'completed': False,
            'link_url': Location('confirmation-group', 0, 'confirmation').url(metadata)
        }
        navigation_links = navigation.build_navigation('property-details', 0)
        self.assertIn(confirmation_link, navigation_links)
        self.assertEqual(len(navigation_links), 5)

    def test_build_navigation_summary_link_not_visible_for_survey_with_confirmation(self):
        schema = load_schema_from_params('test', 'navigation_confirmation')
        schema.answer_is_in_repeating_group = MagicMock(return_value=True)

        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        completed_blocks = [
            Location('property-details', 0, 'insurance-type'),
            Location('property-details', 0, 'insurance-address'),
            Location('property-details', 0, 'property-interstitial'),
            Location('house-details', 0, 'house-type'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('repeating-group', 0, 'repeating-block-1'),
            Location('repeating-group', 0, 'repeating-block-2'),
            Location('extra-cover', 0, 'extra-cover-block'),
            Location('extra-cover', 0, 'extra-cover-interstitial'),
            Location('payment-details', 0, 'credit-card'),
            Location('payment-details', 0, 'expiry-date'),
            Location('payment-details', 0, 'security-code'),
            Location('payment-details', 0, 'security-code-interstitial'),
            Location('extra-cover-items-group', 0, 'extra-cover-items'),
        ]

        navigation = _create_navigation(schema, AnswerStore(), metadata, completed_blocks, [])

        confirmation_link = {
            'link_name': 'Summary',
            'highlight': False,
            'repeating': False,
            'completed': False,
            'link_url': Location('summary-group', 0, 'summary').url(metadata)
        }

        self.assertNotIn(confirmation_link, navigation.build_navigation('property-details', 0))

    def test_build_navigation_submit_answers_link_not_visible_when_no_completed_blocks(self):
        schema = load_schema_from_params('test', 'navigation')
        schema.answer_is_in_repeating_group = MagicMock(return_value=True)

        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        completed_blocks = []
        routing_path = []

        navigation = _create_navigation(schema, AnswerStore(), metadata, completed_blocks, routing_path)

        confirmation_link = {
            'link_name': 'Summary',
            'highlight': False,
            'repeating': False,
            'completed': False,
            'link_url': Location('summary-group', 0, 'summary').url(metadata)
        }

        navigation_links = navigation.build_navigation('property-details', 0)
        self.assertNotIn(confirmation_link, navigation_links)
        self.assertEqual(len(navigation_links), 4)

    def test_build_navigation_summary_link_hidden_when_not_on_routing_path(self):
        schema = load_schema_from_params('test', 'navigation')
        schema.answer_is_in_repeating_group = MagicMock(return_value=True)

        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        completed_blocks = [
            Location('property-details', 0, 'insurance-type'),
            Location('property-details', 0, 'insurance-address'),
            Location('property-details', 0, 'property-interstitial'),
            Location('house-details', 0, 'house-type'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('repeating-group', 0, 'repeating-block-1'),
            Location('repeating-group', 0, 'repeating-block-2'),
            Location('extra-cover', 0, 'extra-cover-block'),
            Location('extra-cover', 0, 'extra-cover-interstitial'),
            Location('payment-details', 0, 'credit-card'),
            Location('payment-details', 0, 'expiry-date'),
            Location('payment-details', 0, 'security-code'),
            Location('payment-details', 0, 'security-code-interstitial'),
            Location('extra-cover-items-group', 0, 'extra-cover-items'),
        ]

        routing_path = [
            Location('property-details', 0, 'insurance-type'),
            Location('property-details', 0, 'insurance-address'),
            Location('property-details', 0, 'property-interstitial'),
            Location('house-details', 0, 'house-type'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('repeating-group', 0, 'repeating-block-1'),
            Location('repeating-group', 0, 'repeating-block-2'),
            Location('payment-details', 0, 'credit-card'),
            Location('payment-details', 0, 'expiry-date'),
            Location('payment-details', 0, 'security-code'),
            Location('payment-details', 0, 'security-code-interstitial'),
            Location('extra-cover', 0, 'extra-cover-block'),
            Location('extra-cover', 0, 'extra-cover-interstitial'),
            Location('extra-cover-items-group', 0, 'extra-cover-items'),
            Location('skip-payment-group', 0, 'skip-payment'),
        ]

        navigation = _create_navigation(schema, AnswerStore(), metadata, completed_blocks, routing_path)

        confirmation_link = {
            'link_name': 'Summary',
            'highlight': False,
            'repeating': False,
            'completed': False,
            'link_url': Location('summary-group', 0, 'summary').url(metadata)
        }

        navigation_links = navigation.build_navigation('property-details', 0)
        self.assertNotIn(confirmation_link, navigation_links)
        self.assertEqual(len(navigation_links), 4)

    def test_build_navigation_summary_link_shown_when_invalid_section_present(self):
        schema = load_schema_from_params('test', 'navigation')
        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        intro_section = {
            'id': 'intro-section',
            'title': 'Intro',
            'groups': [{
                'id': 'intro-group',
                'blocks': [{
                    'id': 'intro-block',
                    'type': 'Interstitial'
                }]
            }]
        }
        schema.json['sections'].insert(0, intro_section)
        # pylint: disable=protected-access
        schema._parse_schema()

        completed_blocks = [
            Location('property-details', 0, 'insurance-type'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('repeating-group', 0, 'repeating-block-1'),
            Location('repeating-group', 0, 'repeating-block-2'),
            Location('skip-payment-group', 0, 'skip-payment'),
        ]

        routing_path = [
            Location('property-details', 0, 'insurance-type'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('repeating-group', 0, 'repeating-block-1'),
            Location('repeating-group', 0, 'repeating-block-2'),
            Location('skip-payment-group', 0, 'skip-payment'),
        ]

        navigation = _create_navigation(schema, AnswerStore(), metadata, completed_blocks, routing_path)

        confirmation_link = {
            'link_name': 'Summary',
            'highlight': False,
            'repeating': False,
            'completed': False,
            'link_url': Location('summary-group', 0, 'summary').url(metadata)
        }

        navigation_links = navigation.build_navigation('skip-payment', 0)

        self.assertIn(confirmation_link, navigation_links)
        self.assertEqual(len(navigation_links), 6)

    def test_build_navigation_repeated_blocks_independent_completeness(self):
        schema = load_schema_from_params('test', 'navigation')
        schema.answer_is_in_repeating_group = MagicMock(return_value=True)

        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        completed_blocks = [
            Location('property-details', 0, 'insurance-type'),
            Location('property-details', 0, 'insurance-address'),
            Location('repeating-group', 0, 'repeating-block-1'),
            Location('repeating-group', 0, 'repeating-block-2'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('extra-cover', 0, 'extra-cover-block')
            ]

        answer_store = AnswerStore()

        answer_store.add(Answer(
            answer_instance=0,
            answer_id='first-name',
            group_instance=0,
            value='Person1'
            ))
        answer_store.add(Answer(
            answer_instance=1,
            answer_id='first-name',
            group_instance=0,
            value='Person2'
            ))
        answer_store.add(Answer(
            answer_instance=0,
            answer_id='what-is-your-age',
            group_instance=0,
            value=42
            ))
        answer_store.add(Answer(
            answer_instance=0,
            answer_id='what-is-your-shoe-size',
            group_instance=0,
            value='Employed'
            ))

        routing_path = [
            Location('property-details', 0, 'insurance-type'),
            Location('property-details', 0, 'insurance-address'),
            Location('repeating-group', 0, 'repeating-block-1'),
            Location('repeating-group', 0, 'repeating-block-2'),
            Location('repeating-group', 1, 'repeating-block-1'),
            Location('repeating-group', 1, 'repeating-block-2'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('extra-cover', 0, 'extra-cover-block'),
            Location('extra-cover-items-group', 0, 'extra-cover-items'),
            Location('skip-payment-group', 0, 'skip-payment'),
            ]

        navigation = _create_navigation(schema, answer_store, metadata, completed_blocks, routing_path)

        user_navigation = [
            {
                'completed': True,
                'highlight': True,
                'repeating': False,
                'link_name': 'Property Details',
                'link_url': Location('property-details', 0, 'insurance-type').url(metadata)
            },
            {
                'link_name': 'Household Composition',
                'highlight': False,
                'repeating': False,
                'completed': True,
                'link_url': Location('multiple-questions-group', 0, 'household-composition').url(metadata)
            },
            {
                'completed': True,
                'highlight': False,
                'repeating': True,
                'link_name': 'Person1',
                'link_url': Location('repeating-group', 0, 'repeating-block-1').url(metadata),
            },
            {
                'completed': False,
                'highlight': False,
                'repeating': True,
                'link_name': 'Person2',
                'link_url': Location('repeating-group', 1, 'repeating-block-1').url(metadata),
            },
            {
                'completed': True,
                'highlight': False,
                'repeating': False,
                'link_name': 'Extra Cover',
                'link_url': Location('extra-cover', 0, 'extra-cover-block').url(metadata),
            },
            {
                'completed': False,
                'highlight': False,
                'repeating': False,
                'link_name': 'Payment Details',
                'link_url': Location('skip-payment-group', 0, 'skip-payment').url(metadata),
            }
        ]

        self.assertEqual(navigation.build_navigation('property-details', 0), user_navigation)

    def test_build_navigation_first_group_with_skip_condition_containing_repeating_group(self):
        schema = load_schema_from_params('test', 'navigation')
        schema.answer_is_in_repeating_group = MagicMock(return_value=True)

        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        # add group to extra-cover-items-section
        schema.json['sections'][6]['groups'].insert(0, {
            'id': 'extra-cover-items-intro',
            'skip_conditions': [{
                'when': [{
                    'id': 'extra-cover-answer',
                    'condition': 'not set'
                }]
            }],
            'blocks': [{
                'id': 'household-full-names-intro-block',
                'type': 'Interstitial'
            }]
        })

        completed_blocks = [
            Location('property-details', 0, 'insurance-type'),
            Location('property-details', 0, 'insurance-address'),
            Location('property-interstitial-section', 0, 'property-interstitial'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('extra-cover', 0, 'extra-cover-block'),
            Location('extra-cover-items-group', 0, 'extra-cover-items'),
        ]

        routing_path = [
            Location('property-details', 0, 'insurance-type'),
            Location('property-details', 0, 'insurance-address'),
            Location('property-interstitial-section', 0, 'property-interstitial'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('extra-cover', 0, 'extra-cover-block'),
            Location('extra-cover-items-group', 0, 'extra-cover-items'),
            Location('skip-payment-group', 0, 'skip-payment'),
        ]

        navigation = _create_navigation(schema, AnswerStore(), metadata, completed_blocks, routing_path)

        user_navigation = [
            {
                'completed': True,
                'highlight': True,
                'repeating': False,
                'link_name': 'Property Details',
                'link_url': Location('property-details', 0, 'insurance-type').url(metadata)
            },
            {
                'link_name': 'Household Composition',
                'highlight': False,
                'repeating': False,
                'completed': True,
                'link_url': Location('multiple-questions-group', 0, 'household-composition').url(metadata)
            },
            # deliberately omitting extra cover section
            {
                'completed': True,
                'highlight': False,
                'repeating': False,
                'link_name': 'Extra Cover',
                'link_url': Location('extra-cover', 0, 'extra-cover-block').url(metadata),
            },
            {
                'completed': False,
                'highlight': False,
                'repeating': False,
                'link_name': 'Payment Details',
                'link_url': Location('skip-payment-group', 0, 'skip-payment').url(metadata),
            }
        ]
        self.assertEqual(navigation.build_navigation(
            'property-details', 0), user_navigation)

    def test_build_navigation_with_single_skipped_block_in_group(self):
        """A section containing a group which doesn't have all of its blocks skipped should
        have its navigation rendered
        """
        schema = load_schema_from_params('test', 'navigation')
        schema.answer_is_in_repeating_group = MagicMock(return_value=True)

        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        # skip the insurance-address block if insurance-type-answer is Both
        schema.json['sections'][0]['groups'][0]['blocks'][1]['skip_conditions'] = [{
            'when': [{
                'id': 'insurance-type-answer',
                'condition': 'equals',
                'value': 'Both'
            }]
        }]

        completed_blocks = [
            Location('property-details', 0, 'insurance-type'),
        ]

        answer_store = AnswerStore()

        answer_store.add(Answer(
            answer_instance=0,
            answer_id='insurance-type-answer',
            group_instance=0,
            value='Both'
        ))

        routing_path = [
            Location('property-details', 0, 'insurance-type'),
            Location('property-details', 0, 'insurance-address'),
            Location('skip-payment-group', 0, 'skip-payment'),
        ]

        navigation = _create_navigation(schema, answer_store, metadata, completed_blocks, routing_path)

        user_navigation = [
            {
                'completed': True,
                'highlight': True,
                'repeating': False,
                'link_name': 'Property Details',
                'link_url': Location('property-details', 0, 'insurance-type').url(metadata)
            },
            {
                'link_name': 'House Details',
                'highlight': False,
                'repeating': False,
                'completed': False,
                'link_url': Location('house-details', 0, 'house-type').url(metadata)
            },
            {
                'link_name': 'Household Composition',
                'highlight': False,
                'repeating': False,
                'completed': False,
                'link_url': Location('multiple-questions-group', 0, 'household-composition').url(metadata)
            },
            {
                'completed': False,
                'highlight': False,
                'repeating': False,
                'link_name': 'Extra Cover',
                'link_url': Location('extra-cover', 0, 'extra-cover-block').url(metadata),
            },
            {
                'completed': False,
                'highlight': False,
                'repeating': False,
                'link_name': 'Payment Details',
                'link_url': Location('skip-payment-group', 0, 'skip-payment').url(metadata),
            }
        ]

        self.assertEqual(navigation.build_navigation('property-details', 0), user_navigation)

    def test_build_navigation_completed_section_with_summary_links_to_last_block(self):
        schema = load_schema_from_params('test', 'navigation_confirmation')
        schema.answer_is_in_repeating_group = MagicMock(return_value=True)

        schema.json['sections'][0]['groups'][0]['blocks'].append({
            'id': 'property-summary',
            'type': 'SectionSummary'
        })

        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        completed_blocks = [
            Location('property-details', 0, 'insurance-type'),
            Location('property-details', 0, 'insurance-address'),
            Location('property-details', 0, 'property-interstitial'),
        ]

        routing_path = [
            Location('property-details', 0, 'insurance-type'),
            Location('property-details', 0, 'insurance-address'),
            Location('property-details', 0, 'property-interstitial'),
            Location('property-details', 0, 'property-summary'),
        ]

        navigation = _create_navigation(schema, AnswerStore(), metadata, completed_blocks, routing_path)

        confirmation_link = {
            'link_name': 'Property Details',
            'highlight': True,
            'repeating': False,
            'completed': True,
            'link_url': Location('property-details', 0, 'property-summary').url(metadata)
        }

        self.assertIn(confirmation_link, navigation.build_navigation('property-details', 0))


def _create_navigation(schema, answer_store, metadata, completed_blocks, routing_path):
    completeness = Completeness(schema, answer_store, completed_blocks, routing_path, metadata)
    return Navigation(schema, answer_store, metadata, completed_blocks, routing_path, completeness)

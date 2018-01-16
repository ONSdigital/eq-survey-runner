from app.data_model.answer_store import AnswerStore, Answer
from app.questionnaire.location import Location
from app.questionnaire.navigation import Navigation
from app.utilities.schema import load_schema_from_params

from tests.app.app_context_test_case import AppContextTestCase


# pylint: disable=R0904,C0302
class TestNavigation(AppContextTestCase):

    def test_navigation_no_blocks_completed(self):
        schema = load_schema_from_params('test', 'navigation')
        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        navigation = Navigation(schema, AnswerStore(), metadata, [], [])

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
        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        answer_store = AnswerStore()

        answer_1 = Answer(
            value='Contents',
            group_instance=0,
            block_id='insurance-type',
            group_id='property-details',
            answer_instance=0,
            answer_id='insurance-type-answer'
        )

        answer_store.add(answer_1)

        completed_blocks = [
            Location('property-details', 0, 'insurance-type'),
            Location('property-details', 0, 'insurance-address')
        ]

        routing_path = [
            Location('property-details', 0, 'insurance-type')
        ]

        navigation = Navigation(schema, answer_store, metadata, completed_blocks, routing_path)

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
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('repeating-group', 0, 'repeating-block-1'),
            Location('repeating-group', 0, 'repeating-block-2'),
            Location('repeating-group', 1, 'repeating-block-1'),
            Location('repeating-group', 1, 'repeating-block-2')
        ]

        navigation = Navigation(schema, AnswerStore(), metadata, completed_blocks, routing_path)

        navigation.answer_store.answers = [
            {
                'group_instance': 0,
                'answer_instance': 0,
                'answer_id': 'first-name',
                'value': 'Jim',
                'group_id': 'multiple-questions-group',
                'block_id': 'household-composition'
            },
            {
                'group_instance': 0,
                'answer_instance': 1,
                'answer_id': 'first-name',
                'value': 'Ben',
                'group_id': 'multiple-questions-group',
                'block_id': 'household-composition'
            },
            {
                'group_instance': 0,
                'answer_instance': 0,
                'answer_id': 'what-is-your-age',
                'value': None,
                'group_id': 'repeating-group',
                'block_id': 'repeating-block-1'
            },
            {
                'group_instance': 0,
                'answer_instance': 0,
                'answer_id': 'what-is-your-shoe-size',
                'value': None,
                'group_id': 'repeating-group',
                'block_id': 'repeating-block-2'
            },
            {
                'group_instance': 1,
                'answer_instance': 0,
                'answer_id': 'what-is-your-age',
                'value': None,
                'group_id': 'repeating-group',
                'block_id': 'repeating-block-1'
            },
            {
                'group_instance': 1,
                'answer_instance': 0,
                'answer_id': 'what-is-your-shoe-size',
                'value': None,
                'group_id': 'repeating-group',
                'block_id': 'repeating-block-2'
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
            group_id='multiple-questions-group',
            answer_id='first-name',
            block_id='household-composition',
            group_instance=0,
            value='Person1'
        )
        answer_2 = Answer(
            answer_instance=1,
            group_id='multiple-questions-group',
            answer_id='first-name',
            block_id='household-composition',
            group_instance=0,
            value='Person2'
        )
        answer_3 = Answer(
            answer_instance=1,
            group_id='extra-cover',
            answer_id='extra-cover-answer',
            block_id='extra-cover-block',
            group_instance=0,
            value=2
        )

        answer_store.add(answer_1)
        answer_store.add(answer_2)
        answer_store.add(answer_3)

        routing_path = [
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('extra-cover', 0, 'extra-cover-block')
        ]

        navigation = Navigation(schema, answer_store, metadata, completed_blocks, routing_path)

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
            group_id='extra-cover',
            block_id='extra-cover-block',
            answer_id='extra-cover-answer',
            answer_instance=0

        )
        answer_2 = Answer(
            value='1',
            group_instance=0,
            group_id='extra-cover-items-group',
            block_id='extra-cover-items',
            answer_id='extra-cover-items-answer',
            answer_instance=0
        )
        answer_3 = Answer(
            value='Yes',
            group_instance=0,
            group_id='extra-cover-items-group',
            block_id='extra-cover-items-radio',
            answer_id='extra-cover-items-radio-answer',
            answer_instance=0
        )
        answer_4 = Answer(
            value='2',
            group_instance=1,
            group_id='extra-cover-items-group',
            block_id='extra-cover-items',
            answer_id='extra-cover-items-answer',
            answer_instance=0
        )
        answer_5 = Answer(
            value='Yes',
            group_instance=1,
            group_id='extra-cover-items-group',
            block_id='extra-cover-items-radio',
            answer_id='extra-cover-items-radio-answer',
            answer_instance=0
        )

        answer_store.add(answer_1)
        answer_store.add(answer_2)
        answer_store.add(answer_3)
        answer_store.add(answer_4)
        answer_store.add(answer_5)

        routing_path = [
            Location('extra-cover', 0, 'extra-cover-block'),
            Location('extra-cover-items-group', 0, 'extra-cover-items'),
            Location('extra-cover-items-group', 0, 'extra-cover-items-radio'),
            Location('extra-cover-items-group', 1, 'extra-cover-items'),
            Location('extra-cover-items-group', 1, 'extra-cover-items-radio')
        ]

        navigation = Navigation(schema, answer_store, metadata, completed_blocks, routing_path)

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
            block_id='household-composition',
            answer_instance=0,
            answer_id='first-name',
            group_id='multiple-questions-group',
            group_instance=0,
            value='Joe'
        )
        answer_2 = Answer(
            block_id='household-composition',
            answer_instance=0,
            answer_id='last-name',
            group_id='multiple-questions-group',
            group_instance=0,
            value='Bloggs'
        )
        answer_3 = Answer(
            block_id='household-composition',
            answer_instance=1,
            answer_id='first-name',
            group_id='multiple-questions-group',
            group_instance=0,
            value='Jane'
        )
        answer_4 = Answer(
            block_id='household-composition',
            answer_instance=1,
            answer_id='last-name',
            group_id='multiple-questions-group',
            group_instance=0,
            value='Doe'
        )

        answer_store.add(answer_1)
        answer_store.add(answer_2)
        answer_store.add(answer_3)
        answer_store.add(answer_4)

        routing_path = [
            Location('multiple-questions-group', 0, 'household-composition')
        ]

        navigation = Navigation(schema, answer_store, metadata, completed_blocks, routing_path)

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
            block_id='insurance-type',
            group_id='property-details',
            answer_instance=0,
            answer_id='insurance-type-answer'
        )

        answer_store.add(answer_1)

        navigation = Navigation(schema, answer_store, metadata, completed_blocks, [])
        user_navigation = navigation.build_navigation('property-details', 0)
        link_names = [d['link_name'] for d in user_navigation]
        self.assertNotIn('Property Interstitial', link_names)

    def test_navigation_skip_condition_show_group(self):
        schema = load_schema_from_params('test', 'navigation')

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
            block_id='insurance-type',
            group_id='property-details',
            answer_instance=0,
            answer_id='insurance-type-answer'
        )

        answer_store.add(answer_1)

        navigation = Navigation(schema, answer_store, metadata, completed_blocks, [])

        user_navigation = navigation.build_navigation('property-details', 0)
        link_names = [d['link_name'] for d in user_navigation]
        self.assertIn('Property Interstitial', link_names)

    def test_navigation_skip_condition_change_answer(self):
        schema = load_schema_from_params('test', 'navigation')

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
            block_id='insurance-type',
            group_id='property-details',
            answer_instance=0,
            answer_id='insurance-type-answer'
        )

        answer_store.add(answer_1)
        navigation = Navigation(schema, answer_store, metadata, completed_blocks, [])

        user_navigation = navigation.build_navigation('property-details', 0)
        link_names = [d['link_name'] for d in user_navigation]
        self.assertIn('Property Interstitial', link_names)

        change_answer = Answer(
            value='Buildings',
            group_instance=0,
            block_id='insurance-type',
            group_id='property-details',
            answer_instance=0,
            answer_id='insurance-type-answer'
        )

        answer_store.update(change_answer)

        user_navigation = navigation.build_navigation('property-details', 0)
        link_names = [d['link_name'] for d in user_navigation]
        self.assertNotIn('Property Interstitial', link_names)

    def test_build_navigation_returns_none_when_schema_navigation_is_false(self):
        # Given
        schema = load_schema_from_params('test', 'navigation')
        schema.json['navigation'] = {'visible': False}
        completed_blocks = []
        metadata = {}
        navigation = Navigation(schema, AnswerStore(), metadata, completed_blocks, [])

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
        navigation = Navigation(schema, AnswerStore(), metadata, completed_blocks, [])

        # When
        nav_menu = navigation.build_navigation('group-1', 'group-instance-1')

        # Then
        self.assertIsNone(nav_menu)

    def test_build_navigation_returns_navigation_when_schema_navigation_is_true(self):
        # Given
        schema = load_schema_from_params('test', 'navigation')
        schema.json['navigation'] = {'visible': True, 'sections': [{'title': 'Nav', 'group_order': ['property-details']}]}
        completed_blocks = []
        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }
        navigation = Navigation(schema, AnswerStore(), metadata, completed_blocks, [])

        # When
        nav_menu = navigation.build_navigation('group-1', 'group-instance-1')

        # Then
        self.assertIsNotNone(nav_menu)

    def test_build_navigation_summary_link_hidden_when_no_sections_completed(self):
        schema = load_schema_from_params('test', 'navigation')
        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        navigation = Navigation(schema, AnswerStore(), metadata, [], [])

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

        navigation = Navigation(schema, AnswerStore(), metadata, completed_blocks, [])

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
            Location('summary-group', 0, 'summary'),
        ]

        navigation = Navigation(schema, AnswerStore(), metadata, completed_blocks, routing_path)

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

        navigation = Navigation(schema, AnswerStore(), metadata, completed_blocks, [])

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
        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        navigation = Navigation(schema, AnswerStore(), metadata, [], [])

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

        navigation = Navigation(schema, AnswerStore(), metadata, completed_blocks, [])

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

        navigation = Navigation(schema, AnswerStore(), metadata, completed_blocks, routing_path)

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

        navigation = Navigation(schema, AnswerStore(), metadata, completed_blocks, [])

        confirmation_link = {
            'link_name': 'Summary',
            'highlight': False,
            'repeating': False,
            'completed': False,
            'link_url': Location('summary-group', 0, 'summary').url(metadata)
        }

        self.assertNotIn(confirmation_link, navigation.build_navigation('property-details', 0))

    def test_build_navigation_summary_link_not_visible_when_hidden_group_not_completed(self):
        schema = load_schema_from_params('test', 'navigation')

        # Payment details group not displayed in navigation
        schema.json['navigation'] = {'sections': [{'title': 'Property Details', 'group_order': ['property-details',
                                                                                                'property-interstitial-group',
                                                                                                'house-details',
                                                                                                'multiple-questions-group',
                                                                                                'repeating-group',
                                                                                                'extra-cover',
                                                                                                'extra-cover-items-group',
                                                                                                'skip-payment-group',
                                                                                                'payment-details']}]}

        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        # Payment details thus not completed
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
            Location('confirmation-group', 0, 'confirmation'),
        ]

        navigation = Navigation(schema, AnswerStore(), metadata, completed_blocks, routing_path)

        confirmation_link = {
            'link_name': 'Summary',
            'highlight': False,
            'repeating': False,
            'completed': False,
            'link_url': Location('summary-group', 0, 'summary').url(metadata)
        }

        navigation_links = navigation.build_navigation('property-details', 0)
        self.assertNotIn(confirmation_link, navigation_links)
        self.assertEqual(len(navigation_links), 1)

    def test_build_navigation_submit_answers_link_not_visible_when_no_completed_blocks(self):
        schema = load_schema_from_params('test', 'navigation')

        metadata = {
            'eq_id': '1',
            'collection_exercise_sid': '999',
            'form_type': 'some_form'
        }

        completed_blocks = []
        routing_path = []

        navigation = Navigation(schema, AnswerStore(), metadata, completed_blocks, routing_path)

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
        ]

        navigation = Navigation(schema, AnswerStore(), metadata, completed_blocks, routing_path)

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

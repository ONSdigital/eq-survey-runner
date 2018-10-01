from unittest.mock import patch
from tests.app.app_context_test_case import AppContextTestCase

from app.data_model.answer_store import AnswerStore, Answer
from app.questionnaire.location import Location
from app.questionnaire.completeness import Completeness
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.utilities.schema import load_schema_from_params


class TestCompleteness(AppContextTestCase): # pylint: disable=too-many-public-methods
    def test_no_groups(self):
        schema = load_schema_from_params('test', 'navigation_completeness')

        schema.json['sections'][0]['groups'] = []

        progress = Completeness(schema, AnswerStore(), [], [], metadata={})

        progress_value = progress.get_state_for_section('coffee-section')
        self.assertEqual(Completeness.NOT_STARTED, progress_value)

    def test_not_started_section(self):
        schema = load_schema_from_params('test', 'navigation_completeness')

        routing_path = [
            Location('coffee-group', 0, 'coffee'),
        ]

        progress = Completeness(schema, AnswerStore(), [], routing_path, metadata={})

        progress_value = progress.get_state_for_section('coffee-section')
        self.assertEqual(Completeness.NOT_STARTED, progress_value)

    def test_started_section(self):
        schema = load_schema_from_params('test', 'navigation_completeness')

        completed_blocks = [
            Location('coffee-group', 0, 'coffee'),
        ]

        routing_path = [
            Location('coffee-group', 0, 'coffee'),
            Location('coffee-group', 0, 'response-yes'),
        ]

        progress = Completeness(
            schema, AnswerStore(), completed_blocks, routing_path, metadata={})

        progress_value = progress.get_state_for_section('coffee-section')
        self.assertEqual(Completeness.STARTED, progress_value)

    def test_completed_section(self):
        schema = load_schema_from_params('test', 'navigation_completeness')

        completed_blocks = [
            Location('coffee-group', 0, 'coffee'),
            Location('coffee-group', 0, 'response-yes'),
        ]

        routing_path = [
            Location('coffee-group', 0, 'coffee'),
            Location('coffee-group', 0, 'response-yes'),
        ]
        progress = Completeness(
            schema, AnswerStore(), completed_blocks, routing_path, metadata={})

        progress_value = progress.get_state_for_section('coffee-section')
        self.assertEqual(Completeness.COMPLETED, progress_value)

    def test_all_sections_complete_no_blocks_completed(self):
        schema = load_schema_from_params('test', 'navigation_completeness')

        routing_path = [
            Location('coffee-group', 0, 'coffee'),
            Location('coffee-group', 0, 'response-yes'),
        ]

        progress = Completeness(schema, AnswerStore(), [], routing_path, metadata={})
        self.assertFalse(progress.all_sections_complete())

    def test_all_sections_complete_one_block_completes(self):
        schema = load_schema_from_params('test', 'navigation_completeness')

        completed_blocks = [
            Location('coffee-group', 0, 'coffee'),
            Location('coffee-group', 0, 'response-yes'),
        ]
        routing_path = [
            Location('coffee-group', 0, 'coffee'),
            Location('coffee-group', 0, 'response-yes'),
            Location('toast-group', 0, 'toast'),
        ]

        progress = Completeness(
            schema, AnswerStore(), completed_blocks, routing_path, metadata={})
        self.assertFalse(progress.all_sections_complete())

    def test_all_sections_complete_all_blocks_completed(self):
        schema = load_schema_from_params('test', 'navigation_completeness')

        completed_blocks = [
            Location('coffee-group', 0, 'coffee'),
            Location('coffee-group', 0, 'response-yes'),
            Location('toast-group', 0, 'toast'),
        ]
        routing_path = [
            Location('coffee-group', 0, 'coffee'),
            Location('coffee-group', 0, 'response-yes'),
            Location('toast-group', 0, 'toast'),
        ]

        progress = Completeness(
            schema, AnswerStore(), completed_blocks, routing_path, metadata={})
        self.assertTrue(progress.all_sections_complete())

    def test_any_section_complete_none(self):
        schema = load_schema_from_params('test', 'navigation_completeness')
        progress = Completeness(schema, AnswerStore(), [], [], metadata={})
        self.assertFalse(progress.any_section_complete())

    def test_any_section_complete_one(self):
        schema = load_schema_from_params('test', 'navigation_completeness')
        completed_blocks = [
            Location('coffee-group', 0, 'coffee'),
            Location('coffee-group', 0, 'response-yes'),
        ]
        routing_path = [
            Location('coffee-group', 0, 'coffee'),
            Location('coffee-group', 0, 'response-yes'),
        ]

        progress = Completeness(
            schema, AnswerStore(), completed_blocks, routing_path, metadata={})
        self.assertTrue(progress.any_section_complete())

    def test_any_section_complete_all(self):
        schema = load_schema_from_params('test', 'navigation_completeness')
        completed_blocks = [
            Location('coffee-group', 0, 'coffee'),
            Location('coffee-group', 0, 'response-yes'),
            Location('toast-group', 0, 'toast'),
        ]
        routing_path = [
            Location('coffee-group', 0, 'coffee'),
            Location('coffee-group', 0, 'response-yes'),
            Location('toast-group', 0, 'toast'),
        ]

        progress = Completeness(
            schema, AnswerStore(), completed_blocks, routing_path, metadata={})
        self.assertTrue(progress.any_section_complete())

    def test_repeating_skipped_group(self):
        schema = load_schema_from_params('test', 'navigation_confirmation')

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

        progress = Completeness(
            schema, AnswerStore(), [], routing_path, metadata={})
        progress_value = progress.get_state_for_group('repeating-group')
        self.assertEqual(Completeness.SKIPPED, progress_value)

    def test_repeating_skipped_section(self):
        schema = load_schema_from_params('test', 'navigation_confirmation')

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


        progress = Completeness(
            schema, AnswerStore(), completed_blocks, routing_path, metadata={})
        progress_value = progress.get_state_for_section(
            'household-full-names-section')
        self.assertEqual(Completeness.SKIPPED, progress_value)

    def test_skipped_group(self):
        schema = load_schema_from_params('test', 'navigation')

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

        progress = Completeness(
            schema, AnswerStore(), completed_blocks, routing_path, metadata={})
        with patch('app.questionnaire.path_finder.evaluate_skip_conditions', return_value=True):
            progress_value = progress.get_state_for_group('payment-details')
        self.assertEqual(Completeness.SKIPPED, progress_value)

    def test_only_question_blocks_counted_for_completeness(self):
        schema_data = {
            'sections': [{
                'id': 'section_1',
                'groups': [{
                    'id': 'group_1',
                    'blocks': [
                        {
                            'id': 'question-block',
                            'type': 'Question',
                            'questions': [{
                                'id': 'question',
                                'title': 'foo',
                                'type': 'general',
                                'answers': []
                            }]
                        },
                        {
                            'id': 'interstitial-block',
                            'type': 'Interstitial',
                            'questions': [{
                                'id': 'interstitial-question',
                                'title': 'bar',
                                'type': 'general',
                                'answers': []
                            }]
                        }
                    ]
                }]
            }]
        }
        schema = QuestionnaireSchema(schema_data)

        completed_blocks = [
            Location('group_1', 0, 'question-block'),
        ]

        routing_path = [
            Location('group_1', 0, 'question-block'),
            Location('group_1', 0, 'interstitial-block'),
        ]

        progress = Completeness(
            schema, AnswerStore(), completed_blocks, routing_path, metadata={})
        self.assertEqual(Completeness.COMPLETED, progress.get_state_for_group('group_1'))
        self.assertEqual(Completeness.COMPLETED, progress.get_state_for_section('section_1'))
        self.assertTrue(progress.all_sections_complete())

    def test_confirmation_questions_checked_for_completeness(self):
        schema_data = {
            'sections': [{
                'id': 'section_1',
                'groups': [{
                    'id': 'group_1',
                    'blocks': [
                        {
                            'id': 'question-block',
                            'type': 'Question',
                            'questions': [{
                                'id': 'question',
                                'title': 'foo',
                                'type': 'general',
                                'answers': []
                            }]
                        },
                        {
                            'id': 'confirm-question-block',
                            'type': 'ConfirmationQuestion',
                            'questions': [{
                                'id': 'confirm-question',
                                'title': 'bar',
                                'type': 'general',
                                'answers': []
                            }]
                        }
                    ]
                }]
            }]
        }
        schema = QuestionnaireSchema(schema_data)

        completed_blocks = [
            Location('group_1', 0, 'question-block'),
        ]

        routing_path = [
            Location('group_1', 0, 'question-block'),
            Location('group_1', 0, 'confirm-question-block'),
        ]

        progress = Completeness(
            schema, AnswerStore(), completed_blocks, routing_path, metadata={})
        self.assertEqual(Completeness.STARTED, progress.get_state_for_group('group_1'))
        self.assertEqual(Completeness.STARTED, progress.get_state_for_section('section_1'))

    def test_get_first_incomplete_location_in_survey_not_started(self):
        schema = load_schema_from_params('test', 'navigation_completeness')
        expected_location = Location('coffee-group', 0, 'coffee')
        routing_path = [
            expected_location,
            Location('coffee-group', 0, 'response-yes'),
        ]

        progress = Completeness(
            schema, AnswerStore(), [], routing_path, metadata={})

        invalid_location = progress.get_first_incomplete_location_in_survey()
        self.assertEqual(expected_location, invalid_location)

    def test_get_first_incomplete_location_in_survey_started(self):
        schema = load_schema_from_params('test', 'navigation_completeness')
        expected_location = Location('coffee-group', 0, 'response-yes')
        completed_blocks = [
            Location('coffee-group', 0, 'coffee'),
        ]

        routing_path = [
            Location('coffee-group', 0, 'coffee'),
            expected_location,
        ]

        progress = Completeness(
            schema, AnswerStore(), completed_blocks, routing_path, metadata={})

        invalid_location = progress.get_first_incomplete_location_in_survey()
        self.assertEqual(expected_location, invalid_location)

    def test_get_first_incomplete_location_in_survey_started_with_repeat(self):
        schema = load_schema_from_params('test', 'navigation')

        completed_blocks = [
            Location('property-details', 0, 'insurance-type'),
            Location('property-details', 0, 'insurance-address'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('extra-cover', 1, 'extra-cover-block'),
            Location('repeating-group', 0, 'repeating-block-1'),
            Location('repeating-group', 1, 'repeating-block-1'),
            Location('repeating-group', 0, 'repeating-block-2'),
            Location('repeating-group', 1, 'repeating-block-2'),
            Location('extra-cover', 0, 'extra-cover-block'),
            Location('extra-cover-items-group', 0, 'extra-cover-items'),
            Location('extra-cover-items-group', 0, 'extra-cover-items-radio'),
        ]

        expected_location = Location('extra-cover-items-group', 1, 'extra-cover-items')
        routing_path = [
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('repeating-group', 0, 'repeating-block-1'),
            Location('repeating-group', 1, 'repeating-block-1'),
            Location('repeating-group', 0, 'repeating-block-2'),
            Location('repeating-group', 1, 'repeating-block-2'),
            Location('extra-cover', 0, 'extra-cover-block'),
            Location('extra-cover-items-group', 0, 'extra-cover-items'),
            Location('extra-cover-items-group', 0, 'extra-cover-items-radio'),
            expected_location,
        ]

        answer_store = AnswerStore()
        answer_store.add(Answer(
            answer_instance=0,
            answer_id='first-name',
            value='Person1'
        ))
        answer_store.add(Answer(
            answer_instance=1,
            answer_id='first-name',
            value='Person2'
        ))
        answer_store.add(Answer(
            answer_instance=0,
            answer_id='extra-cover-answer',
            value=2
        ))

        progress = Completeness(
            schema, answer_store, completed_blocks, routing_path, metadata={})

        with patch('app.questionnaire.path_finder.evaluate_goto', return_value=True):
            invalid_location = progress.get_first_incomplete_location_in_survey()
        self.assertEqual(expected_location, invalid_location)

    def test_get_first_incomplete_location_in_survey_completed(self):
        schema = load_schema_from_params('test', 'navigation')

        # interstitial blocks have been removed
        completed_blocks = [
            Location('property-details', 0, 'insurance-type'),
            Location('property-details', 0, 'insurance-address'),
            Location('house-details', 0, 'house-type'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('repeating-group', 0, 'repeating-block-1'),
            Location('repeating-group', 0, 'repeating-block-2'),
            Location('extra-cover', 0, 'extra-cover-block'),
            Location('payment-details', 0, 'credit-card'),
            Location('payment-details', 0, 'expiry-date'),
            Location('payment-details', 0, 'security-code'),
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
            Location('extra-cover', 0, 'extra-cover-block'),
            Location('extra-cover', 0, 'extra-cover-interstitial'),
            Location('payment-details', 0, 'credit-card'),
            Location('payment-details', 0, 'expiry-date'),
            Location('payment-details', 0, 'security-code'),
            Location('payment-details', 0, 'security-code-interstitial'),
            Location('extra-cover-items-group', 0, 'extra-cover-items'),
            Location('extra-cover-items-group', 0, 'extra-cover-items-radio'),
            Location('skip-payment-group', 0, 'skip-payment'),
            Location('confirmation-group', 0, 'confirmation'),
        ]
        progress = Completeness(
            schema, AnswerStore(), completed_blocks, routing_path, metadata={})
        with patch('app.questionnaire.path_finder.evaluate_goto', return_value=False):
            self.assertFalse(progress.get_first_incomplete_location_in_survey())

    def test_get_state_for_section(self):
        """
        This is a bad test that is really only for coverage.
        The test navigation schema should be changed to include a situation where all groups
        in a section are 'invalid' AND 'skipped'
        """
        with patch('app.questionnaire.completeness.Completeness.get_state_for_group', side_effect=['SKIPPED', 'INVALID']):
            completeness = Completeness([], [], [], [], [])
            self.assertEqual(completeness.get_state_for_section({'id': 'section_id', 'groups': [1, 1]}), 'SKIPPED')

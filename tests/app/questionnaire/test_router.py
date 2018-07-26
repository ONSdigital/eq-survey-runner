from unittest import TestCase
from unittest.mock import MagicMock

from app.questionnaire.router import Router
from app.questionnaire.location import Location
from app.questionnaire.completeness import Completeness
from app.utilities.schema import load_schema_from_params


class TestRouter(TestCase):
    def test_location_is_valid_and_accessible(self):
        schema = load_schema_from_params('test', 'is_skipping_to_end')

        current_location = Location('test-skipping-group', 0, 'test-skipping-forced')

        routing_path = [
            Location('test-skipping-group', 0, 'test-skipping-forced'),
            Location('test-skipping-section-summary-group', 0, 'test-skipping-section-summary'),
            Location('summary-group', 0, 'summary')
        ]

        completeness = Completeness(schema, answer_store=MagicMock(), completed_blocks=[], routing_path=routing_path, metadata={})
        router = Router(schema, routing_path, completeness, current_location)

        self.assertTrue(router.can_access_location())
        self.assertEqual(routing_path[0], router.get_next_location())

    def test_is_not_valid_location(self):
        schema = load_schema_from_params('test', 'is_skipping_to_end')

        current_location = Location('not-in-path', 0, 'not-in-path')

        routing_path = [
            Location('test-skipping-group', 0, 'test-skipping-forced'),
            Location('test-skipping-section-summary-group', 0, 'test-skipping-section-summary'),
            Location('summary-group', 0, 'summary')
        ]

        completed_blocks = [
            Location('test-skipping-group', 0, 'test-skipping-forced')
        ]

        completeness = Completeness(schema, answer_store=MagicMock(), completed_blocks=completed_blocks, routing_path=routing_path, metadata={})
        router = Router(schema, routing_path, completeness, current_location)

        self.assertFalse(router.can_access_location())

        router = Router(schema, routing_path, completeness)

        self.assertFalse(router.can_access_location())
        # Currently, section summary is not added to completed_blocks without POST, ie when using nav bar.
        self.assertEqual(routing_path[2], router.get_next_location())

    def test_get_next_location_invalid_current_location(self):
        schema = load_schema_from_params('test', 'is_skipping_to_end')

        current_location = Location('not-in-path', 0, 'not-in-path')

        routing_path = [
            Location('test-skipping-group', 0, 'test-skipping-forced'),
            Location('test-skipping-section-summary-group', 0, 'test-skipping-section-summary'),
            Location('summary-group', 0, 'summary')
        ]

        completeness = Completeness(schema, answer_store=MagicMock(), completed_blocks=[], routing_path=routing_path, metadata={})
        router = Router(schema, routing_path, completeness, current_location)

        self.assertEqual(routing_path[0], router.get_next_location())

    def test_get_next_location_no_completed_blocks(self):
        schema = load_schema_from_params('test', 'is_skipping_to_end')

        current_location = Location('test-skipping-group', 0, 'test-skipping-forced')

        routing_path = [
            Location('test-skipping-group', 0, 'test-skipping-forced')
        ]

        completeness = Completeness(schema, answer_store=MagicMock(), completed_blocks=[], routing_path=routing_path, metadata={})
        router = Router(schema, routing_path, completeness, current_location)

        self.assertEqual(routing_path[0], router.get_next_location())

    def test_get_next_location_some_completed_blocks(self):
        schema = load_schema_from_params('test', 'is_skipping_to_end')

        current_location = Location('test-skipping-group', 0, 'test-skipping-forced')

        routing_path = [
            Location('test-skipping-group', 0, 'test-skipping-forced'),
            Location('test-skipping-section-summary-group', 0, 'test-skipping-section-summary'),
            Location('test-skipping-group-2', 0, 'test-skipping-forced-2'),
            Location('test-skipping-section-summary-group-2', 0, 'test-skipping-section-summary-2'),
            Location('summary-group', 0, 'test-skipping-forced')
        ]

        completed_blocks = [
            Location('test-skipping-group', 0, 'test-skipping-forced'),
            Location('test-skipping-section-summary-group', 0, 'test-skipping-section-summary'),
        ]

        completeness = Completeness(schema, answer_store=MagicMock(), completed_blocks=completed_blocks, routing_path=routing_path, metadata={})
        router = Router(schema, routing_path, completeness, current_location)

        self.assertEqual(routing_path[2], router.get_next_location())

    def test_skipping_to_end_of_section_no_completed_blocks(self):
        schema = load_schema_from_params('test', 'is_skipping_to_end')

        current_location = Location('test-skipping-section-summary-group', 0, 'test-skipping-section-summary')

        routing_path = [
            Location('test-skipping-group', 0, 'test-skipping-forced'),
            Location('test-skipping-section-summary-group', 0, 'test-skipping-section-summary'),
            Location('summary-group', 0, 'summary')
        ]

        completeness = Completeness(schema, answer_store=MagicMock(), completed_blocks=[], routing_path=routing_path, metadata={})
        router = Router(schema, routing_path, completeness, current_location)

        self.assertFalse(router.can_access_location())

    def test_skipping_to_end_of_survey_no_completed_blocks(self):
        schema = load_schema_from_params('test', 'is_skipping_to_end')

        current_location = Location('summary-group', 0, 'summary')

        routing_path = [
            Location('test-skipping-group', 0, 'test-skipping-forced'),
            Location('test-skipping-section-summary-group', 0, 'test-skipping-section-summary'),
            Location('summary-group', 0, 'summary')
        ]

        completeness = Completeness(schema, answer_store=MagicMock(), completed_blocks=[], routing_path=routing_path, metadata={})
        router = Router(schema, routing_path, completeness, current_location)

        self.assertFalse(router.can_access_location())

    def test_skipping_to_end_of_section_some_completed_blocks(self):
        schema = load_schema_from_params('test', 'is_skipping_to_end')

        current_location = Location('test-skipping-section-summary-group-2', 0, 'test-skipping-section-summary-2')

        routing_path = [
            Location('test-skipping-group', 0, 'test-skipping-forced'),
            Location('test-skipping-group', 0, 'test-skipping-optional'),
            Location('test-skipping-section-summary-group', 0, 'test-skipping-section-summary'),
            Location('test-skipping-group-2', 0, 'test-skipping-forced-2'),
            Location('test-skipping-group-2', 0, 'test-skipping-optional-2'),
            Location('test-skipping-section-summary-group-2', 0, 'test-skipping-section-summary-2'),
            Location('summary-group', 0, 'summary')
        ]

        completed_blocks = [
            Location('test-skipping-group', 0, 'test-skipping-forced'),
            Location('test-skipping-group-2', 0, 'test-skipping-forced-2')
        ]

        completeness = Completeness(schema, answer_store=MagicMock(), completed_blocks=completed_blocks, routing_path=routing_path, metadata={})
        router = Router(schema, routing_path, completeness, current_location)

        self.assertFalse(router.can_access_location())
        self.assertEqual(routing_path[4], router.get_next_location())

    def test_skipping_to_end_of_survey_some_completed_blocks(self):
        schema = load_schema_from_params('test', 'is_skipping_to_end')

        current_location = Location('summary-group', 0, 'summary')

        routing_path = [
            Location('test-skipping-group', 0, 'test-skipping-forced'),
            Location('test-skipping-group', 0, 'test-skipping-optional'),
            Location('test-skipping-section-summary-group', 0, 'test-skipping-section-summary'),
            Location('test-skipping-group-2', 0, 'test-skipping-forced-2'),
            Location('test-skipping-group-2', 0, 'test-skipping-optional-2'),
            Location('test-skipping-section-summary-group-2', 0, 'test-skipping-section-summary-2'),
            Location('summary-group', 0, 'summary')
        ]

        completed_blocks = [
            Location('test-skipping-group', 0, 'test-skipping-forced'),
            Location('test-skipping-group-2', 0, 'test-skipping-forced-2')
        ]

        completeness = Completeness(schema, answer_store=MagicMock(), completed_blocks=completed_blocks, routing_path=routing_path, metadata={})
        router = Router(schema, routing_path, completeness, current_location)

        self.assertFalse(router.can_access_location())
        self.assertEqual(routing_path[1], router.get_next_location())

    def test_section_summary_accessible_when_section_complete(self):
        schema = load_schema_from_params('test', 'is_skipping_to_end')

        current_location = Location('test-skipping-section-summary-group-2', 0, 'test-skipping-section-summary-2')

        routing_path = [
            Location('test-skipping-group', 0, 'test-skipping-forced'),
            Location('test-skipping-group', 0, 'test-skipping-optional'),
            Location('test-skipping-section-summary-group', 0, 'test-skipping-section-summary'),
            Location('test-skipping-group-2', 0, 'test-skipping-forced-2'),
            Location('test-skipping-group-2', 0, 'test-skipping-optional-2'),
            Location('test-skipping-section-summary-group-2', 0, 'test-skipping-section-summary-2'),
            Location('summary-group', 0, 'summary')
        ]

        completed_blocks = [
            Location('test-skipping-group', 0, 'test-skipping-forced'),
            Location('test-skipping-group-2', 0, 'test-skipping-forced-2'),
            Location('test-skipping-group-2', 0, 'test-skipping-optional-2'),
            Location('test-skipping-section-summary-group-2', 0, 'test-skipping-section-summary-2')
        ]

        completeness = Completeness(schema, answer_store=MagicMock(), completed_blocks=completed_blocks, routing_path=routing_path, metadata={})
        router = Router(schema, routing_path, completeness, current_location)

        self.assertTrue(router.can_access_location())
        self.assertEqual(routing_path[1], router.get_next_location())

    def test_final_summary_accessible_when_survey_complete(self):
        schema = load_schema_from_params('test', 'is_skipping_to_end')

        current_location = Location('summary-group', 0, 'summary')

        routing_path = [
            Location('test-skipping-group', 0, 'test-skipping-forced'),
            Location('test-skipping-group', 0, 'test-skipping-optional'),
            Location('test-skipping-section-summary-group', 0, 'test-skipping-section-summary'),
            Location('test-skipping-group-2', 0, 'test-skipping-forced-2'),
            Location('test-skipping-group-2', 0, 'test-skipping-optional-2'),
            Location('test-skipping-section-summary-group-2', 0, 'test-skipping-section-summary-2'),
            Location('summary-group', 0, 'summary')
        ]

        completed_blocks = [
            Location('test-skipping-group', 0, 'test-skipping-forced'),
            Location('test-skipping-group', 0, 'test-skipping-forced'),
            Location('test-skipping-group', 0, 'test-skipping-optional'),
            Location('test-skipping-section-summary-group', 0, 'test-skipping-section-summary'),
            Location('test-skipping-group-2', 0, 'test-skipping-forced-2'),
            Location('test-skipping-group-2', 0, 'test-skipping-optional-2'),
            Location('test-skipping-section-summary-group-2', 0, 'test-skipping-section-summary-2')
        ]

        completeness = Completeness(schema, answer_store=MagicMock(), completed_blocks=completed_blocks, routing_path=routing_path, metadata={})
        router = Router(schema, routing_path, completeness, current_location)

        self.assertTrue(router.can_access_location())
        self.assertEqual(routing_path[-1], router.get_next_location())

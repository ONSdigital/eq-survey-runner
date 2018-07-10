from unittest.mock import MagicMock

from tests.app.app_context_test_case import AppContextTestCase
from app.questionnaire.router import Router
from app.questionnaire.location import Location
from app.questionnaire.completeness import Completeness
from app.utilities.schema import load_schema_from_params


class TestRouter(AppContextTestCase):
    def test_location_is_valid_and_accessible(self):
        schema = load_schema_from_params('test', 'is_skipping_question')
        section = schema.get_section_by_block_id('test-skipping-section-summary')
        block = schema.get_block('test-skipping-section-summary')

        current_location = Location('test-skipping-group', 0, 'test-skipping-forced')

        routing_path = [
            Location('test-skipping-group', 0, 'test-skipping-forced'),
            Location('test-skipping-section-summary-group', 0, 'test-skipping-section-summary'),
            Location('summary-group', 0, 'summary')
        ]

        completness = Completeness(schema, answer_store=MagicMock(), completed_blocks=[], routing_path=routing_path, metadata={})
        route = Router(current_location, routing_path, completness)

        self.assertTrue(route.is_valid_location())
        self.assertTrue(route.can_access_location(section, block))

    def test_is_not_valid_location(self):
        schema = load_schema_from_params('test', 'is_skipping_question')
        current_location = Location('not-in-path', 0, 'not-in-path')

        routing_path = [
            Location('test-skipping-group', 0, 'test-skipping-forced'),
            Location('test-skipping-section-summary-group', 0, 'test-skipping-section-summary'),
            Location('summary-group', 0, 'summary')
        ]

        completness = Completeness(schema, answer_store=MagicMock(), completed_blocks=[], routing_path=routing_path, metadata={})
        route = Router(current_location, routing_path, completness)

        self.assertFalse(route.is_valid_location())

    def test_skipping_to_end_of_section(self):
        schema = load_schema_from_params('test', 'is_skipping_question')
        section = schema.get_section_by_block_id('test-skipping-section-summary')
        block = schema.get_block('test-skipping-section-summary')

        current_location = Location('test-skipping-section-summary-group', 0, 'test-skipping-section-summary')

        routing_path = [
            Location('test-skipping-group', 0, 'test-skipping-forced'),
            Location('test-skipping-section-summary-group', 0, 'test-skipping-section-summary'),
            Location('summary-group', 0, 'summary')
        ]

        completness = Completeness(schema, answer_store=MagicMock(), completed_blocks=[], routing_path=routing_path, metadata={})
        route = Router(current_location, routing_path, completness)

        self.assertFalse(route.can_access_location(section, block))

    def test_skipping_to_end_of_survey(self):
        schema = load_schema_from_params('test', 'is_skipping_question')
        section = schema.get_section_by_block_id('test-skipping-section-summary')
        block = schema.get_block('test-skipping-section-summary')

        current_location = Location('summary-group', 0, 'summary')

        routing_path = [
            Location('test-skipping-group', 0, 'test-skipping-forced'),
            Location('test-skipping-section-summary-group', 0, 'test-skipping-section-summary'),
            Location('summary-group', 0, 'summary')
        ]

        completness = Completeness(schema, answer_store=MagicMock(), completed_blocks=[], routing_path=routing_path, metadata={})
        route = Router(current_location, routing_path, completness)

        self.assertFalse(route.can_access_location(section, block))

    def test_get_next_location_invalid_current_location(self):
        schema = load_schema_from_params('test', 'is_skipping_question')
        current_location = Location('not-in-path', 0, 'not-in-path')
        expected_location = Location('test-skipping-group', 0, 'test-skipping-forced')

        routing_path = [
            expected_location,
            Location('test-skipping-section-summary-group', 0, 'test-skipping-section-summary'),
            Location('summary-group', 0, 'summary')
        ]

        completness = Completeness(schema, answer_store=MagicMock(), completed_blocks=[], routing_path=routing_path, metadata={})
        route = Router(current_location, routing_path, completness)

        self.assertEqual(expected_location, route.get_next_location())

    def test_get_first_incomplete_block_in_section_when_skipping_to_section_summary(self):
        schema = load_schema_from_params('test', 'is_skipping_question')
        section = schema.get_section_by_block_id('test-skipping-section-summary-2')
        block = schema.get_block('test-skipping-section-summary-2')

        current_location = Location('test-skipping-section-summary-group-2', 0, 'test-skipping-section-summary-2')
        expected_location = Location('test-skipping-group-2', 0, 'test-skipping-optional-2')

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

        completness = Completeness(schema, answer_store=MagicMock(), completed_blocks=completed_blocks, routing_path=routing_path, metadata={})
        route = Router(current_location, routing_path, completness)

        self.assertFalse(route.can_access_location(section, block))
        self.assertEqual(expected_location, route.get_next_location())

    def test_get_first_incomplete_block_in_survey_when_skipping_to_end_of_survey(self):
        schema = load_schema_from_params('test', 'is_skipping_question')
        section = schema.get_section_by_block_id('summary')
        block = schema.get_block('summary')

        current_location = Location('summary-group', 0, 'summary')
        expected_location = Location('test-skipping-group', 0, 'test-skipping-optional')

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

        completness = Completeness(schema, answer_store=MagicMock(), completed_blocks=completed_blocks, routing_path=routing_path, metadata={})
        route = Router(current_location, routing_path, completness)

        self.assertFalse(route.can_access_location(section, block))
        self.assertEqual(expected_location, route.get_next_location())

    def test_section_summary_accessible_when_section_complete(self):
        schema = load_schema_from_params('test', 'is_skipping_question')
        section = schema.get_section_by_block_id('test-skipping-section-summary-2')
        block = schema.get_block('test-skipping-section-summary-2')

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

        completness = Completeness(schema, answer_store=MagicMock(), completed_blocks=completed_blocks, routing_path=routing_path, metadata={})
        route = Router(current_location, routing_path, completness)

        self.assertTrue(route.can_access_location(section, block))

    def test_final_summary_accessible_when_survey_complete(self):
        schema = load_schema_from_params('test', 'is_skipping_question')
        section = schema.get_section_by_block_id('summary')
        block = schema.get_block('summary')

        current_location = Location('summary', 0, 'summary')

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

        completness = Completeness(schema, answer_store=MagicMock(), completed_blocks=completed_blocks, routing_path=routing_path, metadata={})
        route = Router(current_location, routing_path, completness)

        self.assertTrue(route.can_access_location(section, block))

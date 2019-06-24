from app.data_model.completed_store import CompletedStore
from app.questionnaire.location import Location
from app.questionnaire.router import Router
from app.utilities.schema import load_schema_from_params
from tests.app.app_context_test_case import AppContextTestCase


class TestRouter(AppContextTestCase):
    def test_can_access_location(self):
        schema = load_schema_from_params('test', 'textfield')
        completed_store = CompletedStore({})
        router = Router(schema, completed_store)

        current_location = Location(block_id='name-block')
        routing_path = [Location(block_id='name-block'), Location(block_id='summary')]
        can_access_location = router.can_access_location(current_location, routing_path)

        self.assertTrue(can_access_location)

    def test_cant_access_location(self):
        schema = load_schema_from_params('test', 'textfield')
        completed_store = CompletedStore({})
        router = Router(schema, completed_store)

        current_location = Location(block_id='name-block')
        routing_path = []
        can_access_location = router.can_access_location(current_location, routing_path)

        self.assertFalse(can_access_location)

    def test_cant_access_location_not_on_allowable_path(self):
        schema = load_schema_from_params('test', 'unit_patterns')
        completed_store = CompletedStore({})
        router = Router(schema, completed_store)

        current_location = Location(block_id='set-duration-units-block')
        routing_path = [
            Location(block_id='set-length-units-block'),
            Location(block_id='set-duration-units-block'),
            Location(block_id='set-area-units-block'),
            Location(block_id='set-volume-units-block'),
            Location(block_id='summary'),
        ]
        can_access_location = router.can_access_location(current_location, routing_path)

        self.assertFalse(can_access_location)

    def test_next_location(self):
        schema = load_schema_from_params('test', 'textfield')
        completed_store = CompletedStore({'sections': ['default-section']})
        router = Router(schema, completed_store)

        current_location = Location(block_id='name-block')
        routing_path = [Location(block_id='name-block'), Location(block_id='summary')]
        next_location = router.get_next_location(current_location, routing_path)
        expected_location = Location(block_id='summary')

        self.assertEqual(next_location, expected_location)

    def test_previous_location(self):
        schema = load_schema_from_params('test', 'textfield')
        completed_store = CompletedStore({})
        router = Router(schema, completed_store)

        current_location = Location(block_id='summary')
        routing_path = [Location(block_id='name-block'), Location(block_id='summary')]
        previous_location = router.get_previous_location(current_location, routing_path)
        expected_location = Location(block_id='name-block')

        self.assertEqual(previous_location, expected_location)

    def test_is_survey_not_complete(self):
        schema = load_schema_from_params('test', 'textfield')
        completed_store = CompletedStore({})
        router = Router(schema, completed_store)

        is_survey_complete = router.is_survey_complete()

        self.assertFalse(is_survey_complete)

    def test_is_survey_complete(self):
        schema = load_schema_from_params('test', 'textfield')
        completed_store = CompletedStore(
            {'blocks': [{'block_id': 'name-block'}], 'sections': ['default-section']}
        )
        router = Router(schema, completed_store)

        is_survey_complete = router.is_survey_complete()

        self.assertTrue(is_survey_complete)

    def test_is_survey_complete_summary_in_own_section(self):
        schema = load_schema_from_params('test', 'placeholder_full')
        completed_store = CompletedStore(
            {
                'blocks': [],
                'sections': [
                    'name-section',
                    'age-input-section',
                    'age-confirmation-section',
                ],
            }
        )
        router = Router(schema, completed_store)

        is_survey_complete = router.is_survey_complete()

        self.assertTrue(is_survey_complete)

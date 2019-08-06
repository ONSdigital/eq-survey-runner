from app.questionnaire.relationship_location import RelationshipLocation

from tests.app.app_context_test_case import AppContextTestCase


class TestRelationshipLocation(AppContextTestCase):
    def test_location_url(self):
        location = RelationshipLocation('relationships', 'id1', 'id2')
        location_url = location.url()

        self.assertEqual(
            location_url,
            'http://test.localdomain/questionnaire/relationships/id1/to/id2/',
        )

    def test_create_location_from_dict(self):
        location_dict = {
            'block_id': 'relationships',
            'list_item_id': 'id1',
            'to_list_item_id': 'id2',
        }

        location = RelationshipLocation(**location_dict)

        self.assertEqual(location.block_id, 'relationships')
        self.assertEqual(location.list_item_id, 'id1')
        self.assertEqual(location.to_list_item_id, 'id2')

    def test_for_json(self):
        location = RelationshipLocation('relationships', 'id1', 'id2')
        json = location.for_json()

        self.assertEqual(
            json,
            {
                'block_id': 'relationships',
                'list_item_id': 'id1',
                'to_list_item_id': 'id2',
            },
        )

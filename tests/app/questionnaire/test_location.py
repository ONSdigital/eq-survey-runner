from app.questionnaire.location import Location

from tests.app.app_context_test_case import AppContextTestCase


class TestLocation(AppContextTestCase):
    def test_location_url(self):
        location = Location(section_id='some-section', block_id='some-block')
        location_url = location.url()

        self.assertEqual(
            location_url, 'http://test.localdomain/questionnaire/some-block/'
        )

    def test_location_url_with_list(self):
        location = Location(
            section_id='some-section', block_id='add-block', list_name='people'
        )
        location_url = location.url()

        self.assertEqual(
            location_url, 'http://test.localdomain/questionnaire/people/add-block/'
        )

    def test_location_url_with_list_item_id(self):
        location = Location(
            section_id='some-section',
            block_id='add-block',
            list_name='people',
            list_item_id='abc123',
        )
        location_url = location.url()

        self.assertEqual(
            location_url,
            'http://test.localdomain/questionnaire/people/abc123/add-block/',
        )

    def test_location_hash(self):
        location = Location(section_id='some-section', block_id='some-block')

        self.assertEqual(hash(location), hash(frozenset(location.__dict__.values())))

    def test_load_location_from_dict(self):
        location_dict = {
            'section_id': 'some-section',
            'block_id': 'some-block',
            'list_name': 'people',
            'list_item_id': 'adhjiiw',
        }

        location = Location.from_dict(location_dict)

        self.assertEqual(location.section_id, 'some-section')
        self.assertEqual(location.block_id, 'some-block')
        self.assertEqual(location.list_item_id, 'adhjiiw')
        self.assertEqual(location.list_name, 'people')

    def test_load_location_from_dict_without_list_item_id(self):
        location_dict = {'section_id': 'some-section', 'block_id': 'some-block'}

        location = Location.from_dict(location_dict)

        self.assertEqual(location.section_id, 'some-section')
        self.assertEqual(location.block_id, 'some-block')
        self.assertEqual(location.list_item_id, None)
        self.assertEqual(location.list_name, None)

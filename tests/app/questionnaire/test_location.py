from app.questionnaire.location import Location

from tests.app.app_context_test_case import AppContextTestCase


class TestLocation(AppContextTestCase):

    def test_location_url(self):
        location = Location('some-block')
        location_url = location.url()

        self.assertEqual(location_url, 'http://test.localdomain/questionnaire/some-block')

    def test_location_hash(self):
        location = Location('some-block')

        self.assertEqual(hash(location), hash(frozenset(location.__dict__.values())))

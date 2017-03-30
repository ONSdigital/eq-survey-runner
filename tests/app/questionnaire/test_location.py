from app.questionnaire.location import Location

from tests.app.app_context_test_case import AppContextTestCase


class TestLocation(AppContextTestCase):

    def test_location_url(self):
        location = Location('some-group', 0, 'some-block')

        metadata = {
            "eq_id": '1',
            "collection_exercise_sid": '999',
            "form_type": "some_form"
        }
        location_url = location.url(metadata)

        self.assertEqual(location_url, "http://test/questionnaire/1/some_form/999/some-group/0/some-block")

import unittest

from app import create_app
from app.questionnaire.location import Location


class TestLocation(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['SERVER_NAME'] = "test"
        self.app_context = self.app.app_context()
        self.app_context.push()

    def test_location_url(self):
        location = Location('some-group', 0, 'some-block')

        metadata = {
            "eq_id": '1',
            "collection_exercise_sid": '999',
            "form_type": "some_form"
        }
        location_url = location.url(metadata)

        self.assertEqual(location_url, "http://test/questionnaire/1/some_form/999/some-group/0/some-block")

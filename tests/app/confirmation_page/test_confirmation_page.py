from app.questionnaire.navigator import Navigator
from app.schema_loader.schema_loader import load_schema_file
import unittest


class TestConfirmationPage(unittest.TestCase):

    def setUp(self):
        survey = load_schema_file("0_rogue_one.json")

        self.navigator = Navigator(survey)

    def test_get_next_location_confirmation(self):
        current_location_id = "5e633f04-073a-44c0-a9da-a7cc2116b937"
        answers = {
            "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c": "Orson Krennic"
        }
        next_location = self.navigator.get_next_location(answers, current_location_id)
        self.assertEqual('summary', next_location)

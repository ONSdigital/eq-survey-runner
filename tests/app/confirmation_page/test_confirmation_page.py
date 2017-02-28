import unittest

from app.data_model.answer_store import Answer, AnswerStore
from app.questionnaire.location import Location
from app.questionnaire.path_finder import PathFinder
from app.schema_loader.schema_loader import load_schema_file


class TestConfirmationPage(unittest.TestCase):

    def test_get_next_location_confirmation(self):
        answer = Answer(
            answer_id="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c",
            value="Orson Krennic",
        )
        answer_store = AnswerStore()
        answer_store.add(answer)

        survey = load_schema_file("0_rogue_one.json")
        navigator = PathFinder(survey, answer_store)
        next_location = navigator.get_next_location(Location('rogue-one-group', 0, 'rogue-one-group-last-block'))

        self.assertEqual('summary', next_location.block_id)

import unittest

from app.data_model.answer_store import Answer, AnswerStore
from app.questionnaire.location import Location
from app.questionnaire.path_finder import PathFinder
from app.utilities.schema import load_schema_file


class TestConfirmationPage(unittest.TestCase):

    def test_get_next_location_confirmation(self):
        answer = Answer(
            answer_id="character-answer",
            value="Orson Krennic",
        )
        answer_store = AnswerStore()
        answer_store.add(answer)

        survey = load_schema_file("0_rogue_one.json")
        navigator = PathFinder(survey, answer_store)
        next_location = navigator.get_next_location(Location('rogue-one', 0, 'film-takings'))

        self.assertEqual('summary', next_location.block_id)

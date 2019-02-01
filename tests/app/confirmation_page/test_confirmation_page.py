from unittest.mock import patch
from app.data_model.answer_store import Answer, AnswerStore
from app.questionnaire.location import Location
from app.questionnaire.path_finder import PathFinder
from app.utilities.schema import load_schema_from_params
from tests.app.app_context_test_case import AppContextTestCase


class TestConfirmationPage(AppContextTestCase):

    def test_get_next_location_confirmation(self):
        answer = Answer(
            answer_id='character-answer',
            value='Orson Krennic',
        )
        answer_store = AnswerStore()
        answer_store.add_or_update(answer)

        schema = load_schema_from_params('test', 'star_wars_rogue_one')
        navigator = PathFinder(schema, answer_store, {}, [])

        with patch('app.questionnaire.rules.evaluate_when_rules', return_value=True):
            next_location = navigator.get_next_location(Location('rogue-one', 0, 'film-takings'))

        self.assertEqual('summary', next_location.block_id)

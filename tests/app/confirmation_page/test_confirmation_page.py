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
        answer_store.add(answer)

        schema = load_schema_from_params('0', 'rogue_one')
        navigator = PathFinder(schema, answer_store, {}, [])
        next_location = navigator.get_next_location(Location('rogue-one', 0, 'film-takings'))

        self.assertEqual('summary', next_location.block_id)

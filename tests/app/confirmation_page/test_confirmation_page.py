from app.questionnaire.navigator import Navigator
from app.data_model.answer_store import Answer, AnswerStore
from app.schema_loader.schema_loader import load_schema_file
import unittest


class TestConfirmationPage(unittest.TestCase):

    def test_get_next_location_confirmation(self):
        last_block_id = "5e633f04-073a-44c0-a9da-a7cc2116b937"
        answer = Answer(
            answer_id="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c",
            value="Orson Krennic",
        )
        answer_store = AnswerStore()
        answer_store.add(answer)

        navigator = Navigator(load_schema_file("0_rogue_one.json"), {}, answer_store)
        next_location = navigator.get_next_location(current_block_id=last_block_id)

        self.assertEqual('summary', next_location['block_id'])

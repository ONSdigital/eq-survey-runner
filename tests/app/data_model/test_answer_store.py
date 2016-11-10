import unittest
from app.data_model.questionnaire_store import AnswerStore


class TestAnswerStore(unittest.TestCase):
    def setUp(self):
        self.store = AnswerStore()

    def test_adds_answer(self):
        answer = {
            'block_id': "3",
            'answer_id': "4",
            'question_id': "5",
            'answer_instance': 1,
            'value': 25,
        }

        self.store.add(answer)

        self.assertEqual(self.store.count(answer), 1)

    def test_finds_answer(self):
        answer = {
            'block_id': "3",
            'answer_id': "4",
            'question_id': "5",
            'answer_instance': 1,
            'value': 25,
        }

        self.store.add(answer)

        self.assertEqual(self.store.find(answer), [answer])

    def test_matches_answer(self):
        answer_1 = {
            'block_id': "3",
            'answer_id': "4",
            'question_id': "5",
            'answer_instance': 1,
            'value': 25,
        }
        answer_2 = {
            'block_id': "3",
            'answer_id': "4",
            'question_id': "5",
            'answer_instance': 1,
            'value': 65,
        }

        self.assertEqual(self.store.same(answer_1, answer_2), True)

    def test_updates_answer(self):
        answer_1 = {
            'block_id': "3",
            'answer_id': "4",
            'question_id': "5",
            'answer_instance': 1,
            'value': 25,
        }
        answer_2 = {
            'block_id': "3",
            'answer_id': "4",
            'question_id': "5",
            'answer_instance': 1,
            'value': 65,
        }

        self.store.add(answer_1)

        self.store.update(answer_2)

        self.assertEqual(self.store.count(answer_2), 1)

        store_match = self.store.find(answer_1)

        self.assertEqual(store_match, [answer_2])

    def test_filters_answers(self):
        answer_1 = {
            'block_id': "1",
            'answer_id': "2",
            'question_id': "3",
            'answer_instance': 1,
            'value': 25,
        }
        answer_2 = {
            'block_id': "1",
            'answer_id': "5",
            'question_id': "6",
            'answer_instance': 1,
            'value': 65,
        }

        self.store.add(answer_1)
        self.store.add(answer_2)

        filtered = self.store.filter({
            'block_id': "1"
        })

        self.assertEqual(len(filtered), 2)

        filtered = self.store.filter({
            'question_id': "6"
        })

        self.assertEqual(len(filtered), 1)

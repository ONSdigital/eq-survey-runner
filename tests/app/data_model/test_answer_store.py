import unittest
from app.data_model.answer_store import AnswerStore


class TestAnswerStore(unittest.TestCase):
    def setUp(self):
        self.store = AnswerStore()

    def tearDown(self):
        self.store.clear()

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

    def test_adds_multidict_answer(self):
        answer = {
            'block_id': "3",
            'answer_id': "4",
            'question_id': "5",
            'answer_instance': 1,
            'value': [23, 45, 67],
        }

        self.store.add(answer)
        found = self.store.find(answer)

        self.assertEqual(found[0]['value'], [23, 45, 67])

        answer = {
            'block_id': "3",
            'answer_id': "4",
            'question_id': "5",
            'answer_instance': 1,
            'value': ['23', '45', '67'],
        }

        self.store.add(answer)
        found = self.store.find(answer)

        self.assertEqual(found[0]['value'], ['23', '45', '67'])

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

    def test_add_inserts_instances(self):
        answer_1 = {
            'block_id': "3",
            'answer_id': "4",
            'question_id': "5",
            'answer_instance': 1,
            'value': 25,
        }
        self.store.add(answer_1)
        answer_1['answer_instance'] = 2

        self.store.add(answer_1)

        answer_1['answer_instance'] = 3

        self.store.add(answer_1)

        self.assertEqual(len(self.store.answers), 3)

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

    def test_maps_answers(self):
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

        expected_answers = {
            "2_1": 25,
            "5_1": 65
        }

        self.assertEqual(self.store.map(), expected_answers)

    def test_maps_and_filters_answers(self):
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

        expected_answers = {
            "5_1": 65
        }

        self.assertEqual(self.store.map({
            "question_id": "6"
        }), expected_answers)

    def test_returns_ordered_map(self):
        answer = {
            'block_id': "1",
            'answer_id': "2",
            'question_id': "3",
            'value': 25,
        }

        for i in range(0, 1000):
            answer['answer_instance'] = i

            self.store.add(answer)

        last_instance = -1

        self.assertEqual(len(self.store.answers), 1000)

        mapped = self.store.map()

        for key, v in mapped.items():
            pos = key.find('_')

            instance = 0 if pos == -1 else int(key[pos + 1:])

            self.assertGreater(instance, last_instance)

            last_instance = instance

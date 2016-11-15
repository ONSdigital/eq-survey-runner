import unittest
from app.data_model.answer_store import Answer, AnswerStore


class TestAnswerStore(unittest.TestCase):
    def setUp(self):
        self.store = AnswerStore()

    def tearDown(self):
        self.store.clear()

    def test_adds_answer(self):
        answer = Answer(
            block_id="3",
            answer_id="4",
            answer_instance=1,
            value=25,
        )

        self.store.add(answer)

        self.assertEqual(self.store.count(answer), 1)

    def test_raises_error_on_invalid(self):
        with self.assertRaises(TypeError) as ite:
            self.store.add({
                "block_id": "3",
                "answer_id":"4",
                "answer_instance": 1,
                "value": 25,
            })

        self.assertIn("Method only supports Answer argument type", str(ite.exception))

    def test_raises_error_on_add_existing(self):
        answer_1 = Answer(
            block_id="3",
            answer_id="4",
            answer_instance=1,
            value=25,
        )
        self.store.add(answer_1)

        with self.assertRaises(ValueError) as ite:
            self.store.add(answer_1)

        self.assertIn("Answer instance already exists in store", str(ite.exception))

    def test_raises_error_on_update_nonexisting(self):
        answer_1 = Answer(
            block_id="3",
            answer_id="4",
            answer_instance=1,
            value=25,
        )

        with self.assertRaises(ValueError) as ite:
            self.store.update(answer_1)

        self.assertIn("Answer instance does not exist in store", str(ite.exception))

    def test_raises_error_on_get_nonexisting(self):
        answer_1 = Answer(
            block_id="3",
            answer_id="4",
            answer_instance=1,
            value=25,
        )

        with self.assertRaises(ValueError) as ite:
            self.store.get(answer_1)

        self.assertIn("Answer instance does not exist in store", str(ite.exception))

    def test_gets_answer(self):
        answer_1 = Answer(
            block_id="3",
            answer_id="4",
            answer_instance=1,
            value=25,
        )

        answer_2 = Answer(
            block_id="4",
            answer_id="5",
            value=56,
        )

        self.store.add(answer_1)
        self.store.add(answer_2)

        self.assertEqual(self.store.get(answer_1), 25)
        self.assertEqual(self.store.get(answer_2), 56)

    def test_adds_multidict_answer(self):
        answer_1 = Answer(
            block_id="3",
            answer_id="4",
            answer_instance=1,
            value=[23, 45, 67],
        )

        self.store.add(answer_1)
        value = self.store.get(answer_1)

        self.assertEqual(value, [23, 45, 67])

    def test_matches_answer(self):
        answer_1 = Answer(
            block_id="3",
            answer_id="4",
            answer_instance=1,
            value=25,
        )
        answer_2 = Answer(
            block_id="3",
            answer_id="4",
            answer_instance=1,
            value=65,
        )

        self.assertEqual(answer_1.matches(answer_2), True)

    def test_add_inserts_instances(self):
        answer_1 = Answer(
            block_id="3",
            answer_id="4",
            answer_instance=1,
            value=25,
        )
        self.store.add(answer_1)

        answer_1.answer_instance = 2

        self.store.add(answer_1)

        answer_1.answer_instance = 3

        self.store.add(answer_1)

        self.assertEqual(len(self.store.answers), 3)

    def test_updates_answer(self):
        answer_1 = Answer(
            block_id="3",
            answer_id="4",
            answer_instance=1,
            value=25,
        )
        answer_2 = Answer(
            block_id="3",
            answer_id="4",
            answer_instance=1,
            value=65,
        )

        self.store.add(answer_1)
        self.store.update(answer_2)

        self.assertEqual(self.store.count(answer_2), 1)

        store_match = self.store.filter(
            block_id="3",
            answer_id="4",
            answer_instance=1,
        )

        self.assertEqual(store_match, [answer_2.__dict__])

    def test_filters_answers(self):

        answer_1 = Answer(
            block_id="1",
            answer_id="2",
            answer_instance=1,
            value=25,
        )
        answer_2 = Answer(
            block_id="1",
            answer_id="5",
            answer_instance=1,
            value=65,
        )

        self.store.add(answer_1)
        self.store.add(answer_2)

        filtered = self.store.filter(block_id="1")

        self.assertEqual(len(filtered), 2)

        filtered = self.store.filter(answer_id="5")

        self.assertEqual(len(filtered), 1)

    def test_maps_answers(self):

        answer_1 = Answer(
            block_id="1",
            answer_id="2",
            answer_instance=1,
            value=25,
        )
        answer_2 = Answer(
            block_id="1",
            answer_id="5",
            answer_instance=1,
            value=65,
        )

        self.store.add(answer_1)
        self.store.add(answer_2)

        expected_answers = {
            "2_1": 25,
            "5_1": 65
        }

        self.assertEqual(self.store.map(), expected_answers)

    def test_maps_and_filters_answers(self):
        answer_1 = Answer(
            block_id="1",
            answer_id="2",
            answer_instance=1,
            value=25,
        )
        answer_2 = Answer(
            block_id="1",
            answer_id="5",
            answer_instance=1,
            value=65,
        )

        self.store.add(answer_1)
        self.store.add(answer_2)

        expected_answers = {
            "5_1": 65
        }

        self.assertEqual(self.store.map(answer_id="5"), expected_answers)

    def test_returns_ordered_map(self):
        answer = Answer(
            block_id="1",
            answer_id="2",
            value=25,
        )

        for i in range(0, 100):
            answer.answer_instance = i

            self.store.add(answer)

        last_instance = -1

        self.assertEqual(len(self.store.answers), 100)

        mapped = self.store.map()

        for key, _ in mapped.items():
            pos = key.find('_')

            instance = 0 if pos == -1 else int(key[pos + 1:])

            self.assertGreater(instance, last_instance)

            last_instance = instance

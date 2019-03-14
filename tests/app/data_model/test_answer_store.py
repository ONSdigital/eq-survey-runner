# pylint: disable=no-self-use
import unittest

from app.data_model.answer_store import Answer, AnswerStore


class TestAnswer(unittest.TestCase):
    def test_raises_error_on_invalid(self):

        with self.assertRaises(ValueError) as ite:
            Answer(None, None)

        self.assertIn("Both 'answer_id' and 'value' must be set for Answer", str(ite.exception))

    def test_matches_answer(self):
        answer_1 = Answer(
            answer_id='4',
            value=25,
        )
        answer_2 = Answer(
            answer_id='4',
            value=65,
        )

        self.assertEqual(answer_1.matches(answer_2), True)

    def test_matches_answer_dict(self):
        answer_1 = Answer(
            answer_id='4',
            value=25,
        )
        answer_2 = {
            'answer_id': '4',
            'value': 25,
        }

        self.assertEqual(answer_1.matches_dict(answer_2), True)


class TestAnswerStore(unittest.TestCase):  # pylint: disable=too-many-public-methods
    def setUp(self):
        self.store = AnswerStore()

    def tearDown(self):
        self.store.clear()

    def test_adds_answer(self):
        answer = Answer(
            answer_id='4',
            value=25,
        )

        self.store.add_or_update(answer)

        self.assertEqual(len(self.store), 1)

    def test_raises_error_on_invalid(self):

        with self.assertRaises(TypeError) as ite:
            self.store.add_or_update({
                'answer_id': '4',
                'value': 25,
            })

        self.assertIn('Method only supports Answer argument type', str(ite.exception))

    def test_updates_answer(self):
        answer_1 = Answer(
            answer_id='4',
            value=25,
        )
        answer_2 = Answer(
            answer_id='4',
            value=65,
        )

        self.store.add_or_update(answer_1)
        self.store.add_or_update(answer_2)

        self.assertEqual(len(self.store), 1)

        store_match = self.store.filter(
            answer_ids=['4'],
        )

        self.assertEqual(store_match, AnswerStore([answer_2.__dict__]))

    def test_filters_answers(self):

        answer_1 = Answer(
            answer_id='2',
            value=25,
        )
        answer_2 = Answer(
            answer_id='5',
            value=65,
        )

        self.store.add_or_update(answer_1)
        self.store.add_or_update(answer_2)

        filtered = self.store.filter(answer_ids=['5'])

        self.assertEqual(len(filtered), 1)

    def test_escaped(self):

        self.store.add_or_update(Answer(
            answer_id='1',
            value=25,
        ))

        self.store.add_or_update(Answer(
            answer_id='2',
            value="'Twenty Five'",
        ))

        escaped = self.store.escaped()

        self.assertEqual(len(escaped), 2)
        self.assertEqual(escaped.filter(answer_ids=['1']).values()[0], 25)
        self.assertEqual(escaped.filter(answer_ids=['2']).values()[0], '&#39;Twenty Five&#39;')

        # answers in the store have not been escaped
        self.assertEqual(self.store.filter(answer_ids=['1']).values()[0], 25)
        self.assertEqual(self.store.filter(answer_ids=['2']).values()[0], "'Twenty Five'")

    def test_filter_answers_does_not_escapes_values(self):

        self.store.add_or_update(Answer(
            answer_id='1',
            value=25,
        ))

        self.store.add_or_update(Answer(
            answer_id='2',
            value="'Twenty Five'",
        ))

        filtered = self.store.filter(['1', '2'])

        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered.filter(answer_ids=['1']).values()[0], 25)
        self.assertEqual(filtered.filter(answer_ids=['2']).values()[0], "'Twenty Five'")

    def test_filter_chaining_escaped(self):

        self.store.add_or_update(Answer(
            answer_id='1',
            value=25,
        ))

        self.store.add_or_update(Answer(
            answer_id='2',
            value="'Twenty Five'",
        ))

        escaped = self.store.filter(answer_ids=['2']).escaped()

        self.assertEqual(len(escaped), 1)
        self.assertEqual(escaped.values()[0], '&#39;Twenty Five&#39;')

        # answers in the store have not been escaped
        self.assertEqual(self.store.filter(answer_ids=['1']).values()[0], 25)
        self.assertEqual(self.store.filter(answer_ids=['2']).values()[0], "'Twenty Five'")

        values = self.store.filter(answer_ids=['2']).escaped().values()

        self.assertEqual(len(values), 1)
        self.assertEqual(values[0], '&#39;Twenty Five&#39;')

    def test_filter_chaining_count(self):

        self.store.add_or_update(Answer(
            answer_id='1',
            value=25,
        ))

        self.store.add_or_update(Answer(
            answer_id='2',
            value="'Twenty Five'",
        ))

        self.assertEqual(self.store.count(), 2)
        self.assertEqual(self.store.filter(answer_ids=['2']).count(), 1)
        self.assertEqual(self.store.filter(answer_ids=['1', '2']).count(), 2)

    def test_remove_all_answers(self):
        answer_1 = Answer(
            answer_id='answer1',
            value=10,
        )
        answer_2 = Answer(
            answer_id='answer2',
            value=20,
        )

        self.store.add_or_update(answer_1)
        self.store.add_or_update(answer_2)

        self.store.clear()
        self.assertEqual(len(self.store), 0)

    def test_remove_answer(self):
        answer_1 = Answer(
            answer_id='answer1',
            value=10,
        )
        answer_2 = Answer(
            answer_id='answer2',
            value=20,
        )

        self.store.add_or_update(answer_1)
        self.store.add_or_update(answer_2)

        self.store.remove_answer(vars(answer_1))
        self.assertEqual(len(self.store), 1)

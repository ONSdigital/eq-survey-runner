import unittest

from app.data_model.answer_store import Answer, AnswerStore
from app.questionnaire.location import Location


class TestAnswer(unittest.TestCase):
    def test_raises_error_on_invalid(self):

        with self.assertRaises(ValueError) as ite:
            Answer()

        self.assertIn("At least one of 'answer_id', 'group_id', 'block_id' or 'value' must be set for Answer", str(ite.exception))

    def test_matches_answer(self):
        answer_1 = Answer(
            block_id='3',
            answer_id='4',
            answer_instance=1,
            group_id='5',
            group_instance=1,
            value=25,
        )
        answer_2 = Answer(
            block_id='3',
            answer_id='4',
            answer_instance=1,
            group_id='5',
            group_instance=1,
            value=65,
        )

        self.assertEqual(answer_1.matches(answer_2), True)

    def test_matches_answer_dict(self):
        answer_1 = Answer(
            block_id='3',
            answer_id='4',
            answer_instance=1,
            group_id='5',
            group_instance=1,
            value=25,
        )
        answer_2 = {
            'block_id': '3',
            'answer_id': '4',
            'answer_instance': 1,
            'group_id': '5',
            'group_instance': 1,
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
            block_id='3',
            answer_id='4',
            answer_instance=1,
            group_id='5',
            group_instance=1,
            value=25,
        )

        self.store.add(answer)

        self.assertEqual(len(self.store.answers), 1)

    def test_raises_error_on_invalid(self):

        with self.assertRaises(TypeError) as ite:
            self.store.add({
                'block_id': '3',
                'answer_id': '4',
                'answer_instance': 1,
                'group_id': '5',
                'group_instance': 1,
                'value': 25,
            })

        self.assertIn('Method only supports Answer argument type', str(ite.exception))

    def test_raises_error_on_add_existing(self):
        answer_1 = Answer(
            block_id='3',
            answer_id='4',
            answer_instance=1,
            group_id='5',
            group_instance=1,
            value=25,
        )
        self.store.add(answer_1)

        with self.assertRaises(ValueError) as ite:
            self.store.add(answer_1)

        self.assertIn('Answer instance already exists in store', str(ite.exception))

    def test_raises_error_on_update_nonexisting(self):
        answer_1 = Answer(
            block_id='3',
            answer_id='4',
            answer_instance=1,
            group_id='5',
            group_instance=1,
            value=25,
        )

        with self.assertRaises(ValueError) as ite:
            self.store.update(answer_1)

        self.assertIn('Answer instance does not exist in store', str(ite.exception))

    def test_add_inserts_instances(self):
        answer_1 = Answer(
            block_id='3',
            answer_id='4',
            answer_instance=1,
            group_id='5',
            group_instance=1,
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
            block_id='3',
            answer_id='4',
            answer_instance=1,
            group_id='5',
            group_instance=1,
            value=25,
        )
        answer_2 = Answer(
            block_id='3',
            answer_id='4',
            answer_instance=1,
            group_id='5',
            group_instance=1,
            value=65,
        )

        self.store.add(answer_1)
        self.store.update(answer_2)

        self.assertEqual(len(self.store.answers), 1)

        store_match = self.store.filter(
            block_id='3',
            answer_id='4',
            answer_instance=1,
            group_id='5',
            group_instance=1,
        )

        self.assertEqual(store_match.answers, [answer_2.__dict__])

    def test_filters_answers(self):

        answer_1 = Answer(
            block_id='1',
            answer_id='2',
            answer_instance=1,
            group_id='5',
            group_instance=1,
            value=25,
        )
        answer_2 = Answer(
            block_id='1',
            answer_id='5',
            answer_instance=1,
            group_id='6',
            group_instance=1,
            value=65,
        )

        self.store.add(answer_1)
        self.store.add(answer_2)

        filtered = self.store.filter(block_id='1')

        self.assertEqual(len(filtered.answers), 2)

        filtered = self.store.filter(answer_id='5')

        self.assertEqual(len(filtered.answers), 1)

        filtered = self.store.filter(group_id='6')

        self.assertEqual(len(filtered.answers), 1)

    def test_filters_answers_by_location(self):
        answer_1 = Answer(
            block_id='1',
            answer_id='2',
            answer_instance=1,
            group_id='5',
            group_instance=1,
            value=25,
        )
        answer_2 = Answer(
            block_id='1',
            answer_id='5',
            answer_instance=1,
            group_id='6',
            group_instance=1,
            value=65,
        )

        self.store.add(answer_1)
        self.store.add(answer_2)

        location = Location('6', 1, '1')

        filtered = self.store.filter_by_location(location)

        self.assertEqual(len(filtered.answers), 1)

    def test_filters_answers_with_limit(self):

        for i in range(1, 50):
            self.store.add(Answer(
                block_id='1',
                answer_id='2',
                answer_instance=i,
                group_id='5',
                group_instance=1,
                value=25,
            ))

        filtered = self.store.filter(limit=True)

        self.assertEqual(len(filtered.answers), 25)

    def test_escaped(self):

        self.store.add(Answer(
            block_id='1',
            answer_id='1',
            answer_instance=0,
            group_id='5',
            group_instance=1,
            value=25,
        ))

        self.store.add(Answer(
            block_id='1',
            answer_id='2',
            answer_instance=0,
            group_id='5',
            group_instance=1,
            value="'Twenty Five'",
        ))

        escaped = self.store.escaped()

        self.assertEqual(len(escaped.answers), 2)
        self.assertEqual(escaped[0]['value'], 25)
        self.assertEqual(escaped[1]['value'], '&#39;Twenty Five&#39;')

        # answers in the store have not been escaped
        self.assertEqual(self.store.answers[0]['value'], 25)
        self.assertEqual(self.store.answers[1]['value'], "'Twenty Five'")

    def test_filter_answers_does_not_escapes_values(self):

        self.store.add(Answer(
            block_id='1',
            answer_id='1',
            answer_instance=0,
            group_id='5',
            group_instance=1,
            value=25,
        ))

        self.store.add(Answer(
            block_id='1',
            answer_id='2',
            answer_instance=0,
            group_id='5',
            group_instance=1,
            value="'Twenty Five'",
        ))

        filtered = self.store.filter()

        self.assertEqual(len(filtered.answers), 2)
        self.assertEqual(filtered[0]['value'], 25)
        self.assertEqual(filtered[1]['value'], "'Twenty Five'")

    def test_filter_chaining_escaped(self):

        self.store.add(Answer(
            block_id='1',
            answer_id='1',
            answer_instance=0,
            group_id='5',
            group_instance=1,
            value=25,
        ))

        self.store.add(Answer(
            block_id='1',
            answer_id='2',
            answer_instance=0,
            group_id='5',
            group_instance=1,
            value="'Twenty Five'",
        ))

        escaped = self.store.filter(answer_id='2').escaped()

        self.assertEqual(len(escaped.answers), 1)
        self.assertEqual(escaped[0]['value'], '&#39;Twenty Five&#39;')

        # answers in the store have not been escaped
        self.assertEqual(self.store[0]['value'], 25)
        self.assertEqual(self.store[1]['value'], "'Twenty Five'")

        values = self.store.filter(answer_id='2').escaped().values()

        self.assertEqual(len(values), 1)
        self.assertEqual(values[0], '&#39;Twenty Five&#39;')

    def test_filter_chaining_count(self):

        self.store.add(Answer(
            block_id='1',
            answer_id='1',
            answer_instance=0,
            group_id='5',
            group_instance=1,
            value=25,
        ))

        self.store.add(Answer(
            block_id='1',
            answer_id='2',
            answer_instance=0,
            group_id='5',
            group_instance=1,
            value="'Twenty Five'",
        ))

        self.assertEqual(self.store.count(), 2)
        self.assertEqual(self.store.filter(answer_id='2').count(), 1)
        self.assertEqual(self.store.filter().count(), 2)

    def tests_upgrade_reformats_date(self):
        questionnaire = {
            'survey_id': '021',
            'data_version': '0.0.2',
            'groups': [{
                'id': 'group1',
                'blocks': [{
                    'id': 'block1',
                    'questions': [{
                        'id': 'question1',
                        'answers': [
                            {
                                'id': 'answer1',
                                'type': 'Date'
                            }
                        ]
                    }]
                }]
            }]
        }

        answers = [
            {
                'block_id': 'block1',
                'answer_id': 'answer1',
                'answer_instance': 0,
                'group_id': 'group1',
                'group_instance': 0,
                'value': '25/12/2017'
            }
        ]

        self.store = AnswerStore(existing_answers=answers)

        self.store.upgrade(current_version=0, schema_json=questionnaire)

        self.assertEqual(self.store.answers[0]['value'], '2017-12-25')

    def tests_upgrade_reformats_month_year_date(self):
        questionnaire = {
            'survey_id': '021',
            'data_version': '0.0.2',
            'groups': [{
                'id': 'group1',
                'blocks': [{
                    'id': 'block1',
                    'questions': [{
                        'id': 'question1',
                        'answers': [
                            {
                                'id': 'answer1',
                                'type': 'MonthYearDate'
                            }
                        ]
                    }]
                }]
            }]
        }

        answers = [
            {
                'block_id': 'block1',
                'answer_id': 'answer1',
                'answer_instance': 0,
                'group_id': 'group1',
                'group_instance': 0,
                'value': '12/2017'
            }
        ]

        self.store = AnswerStore(existing_answers=answers)

        self.store.upgrade(current_version=0, schema_json=questionnaire)

        self.assertEqual(self.store.answers[0]['value'], '2017-12')

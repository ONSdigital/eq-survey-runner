import unittest
from unittest.mock import patch, MagicMock

from app.data_model.answer_store import Answer, AnswerStore, upgrade_0_to_1_update_date_formats, upgrade_1_to_2_add_group_instance_id
from app.questionnaire.questionnaire_schema import QuestionnaireSchema


class TestAnswer(unittest.TestCase):
    def test_raises_error_on_invalid(self):

        with self.assertRaises(ValueError) as ite:
            Answer(None, None)

        self.assertIn("Both 'answer_id' and 'value' must be set for Answer", str(ite.exception))

    def test_matches_answer(self):
        answer_1 = Answer(
            answer_id='4',
            answer_instance=1,
            group_instance=1,
            value=25,
        )
        answer_2 = Answer(
            answer_id='4',
            answer_instance=1,
            group_instance=1,
            value=65,
        )

        self.assertEqual(answer_1.matches(answer_2), True)

    def test_matches_answer_dict(self):
        answer_1 = Answer(
            answer_id='4',
            answer_instance=1,
            group_instance=1,
            group_instance_id='foo-1',
            value=25,
        )
        answer_2 = {
            'answer_id': '4',
            'answer_instance': 1,
            'group_instance_id': 'foo-1',
            'group_instance': 1,
            'value': 25,
        }

        self.assertEqual(answer_1.matches_dict(answer_2), True)


    def test_matches_answer_dict_missing_key(self):
        # No group_instance_id
        answer_1 = Answer(
            answer_id='4',
            answer_instance=1,
            group_instance=1,
            value=25,
        )
        # No group_instance_id
        answer_2 = {
            'answer_id': '4',
            'answer_instance': 1,
            'group_instance': 1,
            'value': 25,
        }

        self.assertEqual(answer_1.matches_dict(answer_2), True)


    def test_matches_new_answer_against_old_answer(self):
        # Has group_instance_id
        answer_1 = Answer(
            answer_id='4',
            answer_instance=1,
            group_instance=1,
            group_instance_id=None,
            value=25,
        )

        # No group_instance_id
        answer_2 = {
            'answer_id': '4',
            'answer_instance': 1,
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
            answer_id='4',
            answer_instance=1,
            group_instance=1,
            value=25,
        )

        self.store.add(answer)

        self.assertEqual(len(self.store.answers), 1)

    def test_raises_error_on_invalid(self):

        with self.assertRaises(TypeError) as ite:
            self.store.add({
                'answer_id': '4',
                'answer_instance': 1,
                'group_instance': 1,
                'value': 25,
            })

        self.assertIn('Method only supports Answer argument type', str(ite.exception))

    def test_raises_error_on_add_existing(self):
        answer_1 = Answer(
            answer_id='4',
            answer_instance=1,
            group_instance=1,
            group_instance_id='group-1',
            value=25,
        )
        self.store.add(answer_1)

        with self.assertRaises(ValueError) as ite:
            self.store.add(answer_1)

        self.assertIn('Answer instance already exists in store', str(ite.exception))

    def test_raises_error_on_update_nonexisting(self):
        answer_1 = Answer(
            answer_id='4',
            answer_instance=1,
            group_instance=1,
            group_instance_id='group-1',
            value=25,
        )

        with self.assertRaises(ValueError) as ite:
            self.store.update(answer_1)

        self.assertIn('Answer instance does not exist in store', str(ite.exception))

    def test_add_inserts_instances(self):
        answer_1 = Answer(
            answer_id='4',
            answer_instance=1,
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
            answer_id='4',
            answer_instance=1,
            group_instance=1,
            value=25,
        )
        answer_2 = Answer(
            answer_id='4',
            answer_instance=1,
            group_instance=1,
            value=65,
        )

        self.store.add(answer_1)
        self.store.update(answer_2)

        self.assertEqual(len(self.store.answers), 1)

        store_match = self.store.filter(
            answer_ids=['4'],
            answer_instance=1,
            group_instance=1,
        )

        self.assertEqual(store_match.answers, [answer_2.__dict__])

    def test_filters_answers(self):

        answer_1 = Answer(
            answer_id='2',
            answer_instance=1,
            group_instance=1,
            value=25,
        )
        answer_2 = Answer(
            answer_id='5',
            answer_instance=1,
            group_instance=1,
            value=65,
        )

        self.store.add(answer_1)
        self.store.add(answer_2)

        filtered = self.store.filter(answer_ids=['5'])

        self.assertEqual(len(filtered.answers), 1)

    def test_filters_answers_with_limit(self):

        for i in range(1, 50):
            self.store.add(Answer(
                answer_id='2',
                answer_instance=i,
                group_instance=1,
                value=25,
            ))

        filtered = self.store.filter(answer_ids=['2'], limit=True)

        self.assertEqual(len(filtered.answers), 25)

    def test_escaped(self):

        self.store.add(Answer(
            answer_id='1',
            answer_instance=0,
            group_instance=1,
            value=25,
        ))

        self.store.add(Answer(
            answer_id='2',
            answer_instance=0,
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
            answer_id='1',
            answer_instance=0,
            group_instance=1,
            value=25,
        ))

        self.store.add(Answer(
            answer_id='2',
            answer_instance=0,
            group_instance=1,
            value="'Twenty Five'",
        ))

        filtered = self.store.filter(['1', '2'])

        self.assertEqual(len(filtered.answers), 2)
        self.assertEqual(filtered[0]['value'], 25)
        self.assertEqual(filtered[1]['value'], "'Twenty Five'")

    def test_filter_chaining_escaped(self):

        self.store.add(Answer(
            answer_id='1',
            answer_instance=0,
            group_instance=1,
            value=25,
        ))

        self.store.add(Answer(
            answer_id='2',
            answer_instance=0,
            group_instance=1,
            value="'Twenty Five'",
        ))

        escaped = self.store.filter(answer_ids=['2']).escaped()

        self.assertEqual(len(escaped.answers), 1)
        self.assertEqual(escaped[0]['value'], '&#39;Twenty Five&#39;')

        # answers in the store have not been escaped
        self.assertEqual(self.store[0]['value'], 25)
        self.assertEqual(self.store[1]['value'], "'Twenty Five'")

        values = self.store.filter(answer_ids=['2']).escaped().values()

        self.assertEqual(len(values), 1)
        self.assertEqual(values[0], '&#39;Twenty Five&#39;')

    def test_filter_chaining_count(self):

        self.store.add(Answer(
            answer_id='1',
            answer_instance=0,
            group_instance=1,
            value=25,
        ))

        self.store.add(Answer(
            answer_id='2',
            answer_instance=0,
            group_instance=1,
            value="'Twenty Five'",
        ))

        self.assertEqual(self.store.count(), 2)
        self.assertEqual(self.store.filter(answer_ids=['2']).count(), 1)
        self.assertEqual(self.store.filter(answer_ids=['1', '2']).count(), 2)

    def tests_upgrade_reformats_date(self):
        questionnaire = {
            'survey_id': '021',
            'data_version': '0.0.2',
            'sections': [{
                'id': 'secetion1',
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
            }]
        }

        answers = [
            {
                'answer_id': 'answer1',
                'answer_instance': 0,
                'group_instance': 0,
                'value': '25/12/2017'
            }
        ]

        self.store = AnswerStore(existing_answers=answers)

        upgrade_0_to_1_update_date_formats(self.store, QuestionnaireSchema(questionnaire))

        self.assertEqual(self.store.answers[0]['value'], '2017-12-25')

    def tests_upgrade_reformats_month_year_date(self):
        questionnaire = {
            'survey_id': '021',
            'data_version': '0.0.2',
            'sections': [{
                'id': 'section1',
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
            }]
        }

        answers = [
            {
                'answer_id': 'answer1',
                'answer_instance': 0,
                'group_instance': 0,
                'value': '12/2017'
            }
        ]

        self.store = AnswerStore(existing_answers=answers)

        upgrade_0_to_1_update_date_formats(self.store, QuestionnaireSchema(questionnaire))

        self.assertEqual(self.store.answers[0]['value'], '2017-12')

    def tests_upgrade_when_answer_no_longer_in_schema_does_not_reformat(self):
        questionnaire = {
            'survey_id': '021',
            'data_version': '0.0.2',
            'sections': [{
                'id': 'section1',
                'groups': [{
                    'id': 'group1',
                    'blocks': [{
                        'id': 'block1',
                        'questions': [{
                            'id': 'question1',
                            'answers': [
                            ]
                        }]
                    }]
                }]
            }]
        }

        answers = [
            {
                'answer_id': 'answer1',
                'answer_instance': 0,
                'group_instance': 0,
                'value': '12/2017'
            }
        ]

        self.store = AnswerStore(existing_answers=answers)

        upgrade_0_to_1_update_date_formats(self.store, QuestionnaireSchema(questionnaire))

        self.assertEqual(self.store.answers[0]['value'], '12/2017')

    def tests_upgrade_when_block_no_longer_in_schema_does_not_reformat(self):
        questionnaire = {
            'survey_id': '021',
            'data_version': '0.0.2',
            'sections': [{
                'id': 'section1',
                'groups': [{
                    'id': 'group1',
                    'blocks': []
                }]
            }]
        }

        answers = [
            {
                'answer_id': 'answer1',
                'answer_instance': 0,
                'group_instance': 0,
                'value': '12/2017'
            }
        ]

        self.store = AnswerStore(existing_answers=answers)

        upgrade_0_to_1_update_date_formats(self.store, QuestionnaireSchema(questionnaire))

        self.assertEqual(self.store.answers[0]['value'], '12/2017')


    def test_upgrade_add_group_instance_id(self):

        survey = {
            'survey_id': '021',
            'data_version': '0.0.2',
            'sections': [{
                'id': 'section1',
                'groups': [{
                    'id': 'group1',
                    'blocks': [{
                        'id': 'block1',
                        'type': 'Question',
                        'questions': [{
                            'id': 'question1',
                            'answers': [
                                {
                                    'id': 'answer1',
                                    'type': 'TextArea'
                                }
                            ]
                        }]
                    }]
                }, {
                    'id': 'group-2',
                    'blocks': [{
                        'id': 'block-2',
                        'type': 'Question'
                    }],
                    'routing_rules':[{
                        'repeat': {
                            'type': 'group',
                            'group_ids': ['group1']
                        }
                    }]
                }]
            }]
        }

        existing_answers = [
            {
                'answer_id': 'answer1',
                'answer_instance': 0,
                'group_instance': 0,
                'value': '12/2017'
            },
            {
                'answer_id': 'answer1',
                'answer_instance': 1,
                'group_instance': 0,
                'value': '12/2017'
            },
            {
                'answer_id': 'answer1',
                'answer_instance': 0,
                'group_instance': 1,
                'value': '12/2017'
            },
        ]

        answer_store = AnswerStore(existing_answers)

        upgrade_1_to_2_add_group_instance_id(answer_store, QuestionnaireSchema(survey))

        self.assertEqual(answer_store[0]['group_instance_id'], answer_store[1]['group_instance_id'])
        self.assertNotEqual(answer_store[0]['group_instance_id'], answer_store[2]['group_instance_id'])


    def test_upgrade_multiple_versions(self):  # pylint: disable=no-self-use

        answer_store = AnswerStore()

        upgrade_0 = MagicMock()
        upgrade_0.__name__ = 'upgrade_0'
        upgrade_1 = MagicMock()
        upgrade_1.__name__ = 'upgrade_1'
        upgrade_2 = MagicMock()
        upgrade_2.__name__ = 'upgrade_2'

        UPGRADE_TRANSFORMS = (
            upgrade_0, upgrade_1, upgrade_2
        )

        schema = MagicMock()

        with patch('app.data_model.answer_store.UPGRADE_TRANSFORMS', UPGRADE_TRANSFORMS):
            answer_store.upgrade(0, schema)

        upgrade_0.assert_called_once_with(answer_store, schema)
        upgrade_1.assert_called_once_with(answer_store, schema)
        upgrade_2.assert_called_once_with(answer_store, schema)

    def test_upgrade_multiple_versions_skipping_already_run(self):  # pylint: disable=no-self-use

        answer_store = AnswerStore()

        upgrade_0 = MagicMock()
        upgrade_0.__name__ = 'upgrade_0'
        upgrade_1 = MagicMock()
        upgrade_1.__name__ = 'upgrade_1'
        upgrade_2 = MagicMock()
        upgrade_2.__name__ = 'upgrade_2'

        UPGRADE_TRANSFORMS = (
            upgrade_0, upgrade_1, upgrade_2
        )

        schema = MagicMock()

        with patch('app.data_model.answer_store.UPGRADE_TRANSFORMS', UPGRADE_TRANSFORMS):
            answer_store.upgrade(1, schema)

        upgrade_0.assert_not_called()
        upgrade_1.assert_called_once_with(answer_store, schema)
        upgrade_2.assert_called_once_with(answer_store, schema)

    def test_remove_all_answers(self):
        answer_1 = Answer(
            answer_id='answer1',
            value=10,
        )
        answer_2 = Answer(
            answer_id='answer2',
            value=20,
        )

        self.store.add(answer_1)
        self.store.add(answer_2)

        self.store.remove()
        self.assertEqual(len(self.store.answers), 0)

from unittest import TestCase
from unittest.mock import MagicMock

import simplejson as json

from app.data_model.answer_store import AnswerStore
from app.data_model.questionnaire_store import QuestionnaireStore
from app.questionnaire.location import Location


def get_basic_input():
    return {
        'METADATA': {
            'test': True
        },
        'ANSWERS': [{
            'answer_id': 'test',
            'value': 'test',
        }],
        'COMPLETED_BLOCKS': [
            {
                'block_id': 'a-test-block',
            }
        ],
        'COLLECTION_METADATA': {
            'test-meta': 'test'
        },
    }


def get_input_answers_dict():
    return {
        'METADATA': {
            'test': True
        },
        'ANSWERS': {
            'test': [{
                'answer_id': 'test',
                'value': 'test'
            }]
        },
        'COMPLETED_BLOCKS': [
            {
                'block_id': 'a-test-block',
            }
        ],
        'COLLECTION_METADATA': {
            'test-meta': 'test'
        },
    }


class TestQuestionnaireStore(TestCase):

    def setUp(self):

        def get_user_data():
            """Fake get_user_data implementation for storage"""
            return self.input_data, 1

        def set_output_data(data):
            self.output_data = data

        # Storage class mocking
        self.storage = MagicMock()
        self.storage.get_user_data = MagicMock(side_effect=get_user_data)
        self.storage.add_or_update = MagicMock(side_effect=set_output_data)

        self.input_data = '{}'
        self.output_data = ''
        self.output_version = None

    def test_questionnaire_store_loads_json(self):
        # Given
        expected = get_basic_input()
        self.input_data = json.dumps(expected)
        # When
        store = QuestionnaireStore(self.storage)
        # Then
        self.assertEqual(store.metadata.copy(), expected['METADATA'])
        self.assertEqual(store.collection_metadata, expected['COLLECTION_METADATA'])
        self.assertEqual(store.answer_store, AnswerStore(expected['ANSWERS']))
        expected_location = expected['COMPLETED_BLOCKS'][0]
        self.assertEqual(len(store.completed_blocks), 1)
        self.assertEqual(store.completed_blocks[0], Location.from_dict(location_dict=expected_location))

    def test_questionnaire_store_loads_answers_as_dict(self):
        # Given
        expected = get_input_answers_dict()
        self.input_data = json.dumps(expected)
        # When
        store = QuestionnaireStore(self.storage, 3)
        # Then
        self.assertEqual(store.metadata.copy(), expected['METADATA'])
        self.assertEqual(store.collection_metadata, expected['COLLECTION_METADATA'])
        self.assertEqual(store.answer_store, AnswerStore(expected['ANSWERS']))
        expected_location = expected['COMPLETED_BLOCKS'][0]
        self.assertEqual(len(store.completed_blocks), 1)
        self.assertEqual(store.completed_blocks[0], Location.from_dict(location_dict=expected_location))

    def test_questionnaire_store_ignores_extra_json(self):
        # Given
        expected = get_basic_input()
        expected['NOT_A_LEGAL_TOP_LEVEL_KEY'] = 'woop_woop_thats_the_sound_of_the_police'
        self.input_data = json.dumps(expected)
        # When
        store = QuestionnaireStore(self.storage)
        # Then
        self.assertEqual(store.metadata.copy(), expected['METADATA'])
        self.assertEqual(store.collection_metadata, expected['COLLECTION_METADATA'])
        self.assertEqual(store.answer_store, AnswerStore(expected['ANSWERS']))
        expected_location = expected['COMPLETED_BLOCKS'][0]
        self.assertEqual(len(store.completed_blocks), 1)
        self.assertEqual(store.completed_blocks[0], Location.from_dict(location_dict=expected_location))

    def test_questionnaire_store_missing_keys(self):
        # Given
        expected = get_basic_input()
        del expected['COMPLETED_BLOCKS']
        self.input_data = json.dumps(expected)
        # When
        store = QuestionnaireStore(self.storage)
        # Then
        self.assertEqual(store.metadata.copy(), expected['METADATA'])
        self.assertEqual(store.collection_metadata, expected['COLLECTION_METADATA'])
        self.assertEqual(store.answer_store, AnswerStore(expected['ANSWERS']))
        self.assertEqual(len(store.completed_blocks), 0)

    def test_questionnaire_store_updates_storage(self):
        # Given
        expected = get_basic_input()
        store = QuestionnaireStore(self.storage)
        store.set_metadata(expected['METADATA'])
        store.answer_store = AnswerStore(expected['ANSWERS'])
        store.collection_metadata = expected['COLLECTION_METADATA']
        store.completed_blocks = [Location.from_dict(expected['COMPLETED_BLOCKS'][0])]

        # When
        store.add_or_update()  # See setUp - populates self.output_data

        # Then
        self.assertEqual(expected, json.loads(self.output_data))

    def test_questionnaire_store_errors_on_invalid_object(self):
        # Given
        class NotSerializable:
            pass

        non_serializable_metadata = {
            'test': NotSerializable()
        }

        expected = get_basic_input()
        store = QuestionnaireStore(self.storage)
        store.set_metadata(non_serializable_metadata)
        store.collection_metadata = expected['COLLECTION_METADATA']
        store.answer_store = AnswerStore(expected['ANSWERS'])
        store.completed_blocks = [Location.from_dict(expected['COMPLETED_BLOCKS'][0])]

        # When / Then
        self.assertRaises(TypeError, store.add_or_update)

    def test_questionnaire_store_deletes(self):
        # Given
        expected = get_basic_input()
        store = QuestionnaireStore(self.storage)
        store.set_metadata(expected['METADATA'])
        store.collection_metadata = expected['COLLECTION_METADATA']
        store.answer_store = AnswerStore(expected['ANSWERS'])
        store.completed_blocks = [Location.from_dict(expected['COMPLETED_BLOCKS'][0])]

        # When
        store.delete()  # See setUp - populates self.output_data

        # Then
        self.assertEqual(store.completed_blocks, [])
        self.assertEqual(store.metadata.copy(), {})
        self.assertEqual(store.answer_store.count(), 0)
        self.assertEqual(store.collection_metadata, {})

    def test_questionnaire_store_removes_completed_location(self):
        # Given
        expected = get_basic_input()
        store = QuestionnaireStore(self.storage)
        location = Location.from_dict(expected['COMPLETED_BLOCKS'][0])
        store.completed_blocks = [location]
        # When
        store.remove_completed_blocks(location=location)
        # Then
        self.assertEqual(store.completed_blocks, [])

    def test_questionnaire_store_removes_completed_location_from_many(self):
        store = QuestionnaireStore(self.storage)
        location = Location('a-test-block')
        location2 = Location('a-test-block')
        store.completed_blocks = [
            location,
            location2,
        ]
        # When
        store.remove_completed_blocks(location=location)
        # Then
        self.assertEqual(store.completed_blocks, [location2])

    def test_questionnaire_store_raises_when_writing_to_metadata(self):
        store = QuestionnaireStore(self.storage)

        with self.assertRaises(TypeError):
            store.metadata['no'] = 'writing'

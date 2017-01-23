import json
import unittest

from mock import Mock

from app.data_model.answer_store import Answer
from app.data_model.questionnaire_store import QuestionnaireStore
from app.questionnaire.location import Location


class TestQuestionnaireStore(unittest.TestCase):

    def test_should_not_be_changed(self):
        # Given
        storage = Mock()
        data = {
            'METADATA': 'test',
            'ANSWERS': [
                {
                    'value': None,
                    'group_id': 'group',
                    'answer_id': 'answer',
                    'block_id': 'block',
                    'group_instance': 0,
                    'answer_instance': 0
                }
            ],
            'COMPLETED_BLOCKS': [Location('group', 'instance', 'block')]
        }
        storage.get_user_data = Mock(return_value=json.dumps(data, default=lambda o: o.__dict__))
        store = QuestionnaireStore(storage)

        # When
        changed = store.has_changed()

        # Then
        self.assertFalse(changed)

    def test_should_be_changed(self):
        # Given
        storage = Mock()
        data = {
            'METADATA': 'test',
            'ANSWERS': [Answer('group', 'block', 'answer').__dict__],
            'COMPLETED_BLOCKS': [Location('group', 'instance', 'block')]
        }
        storage.get_user_data = Mock(return_value=json.dumps(data, default=lambda o: o.__dict__))
        store = QuestionnaireStore(storage)
        store.answer_store.add(Answer('group_id', 'block_id', 'answer_id'))

        # When
        changed = store.has_changed()

        # Then
        self.assertTrue(changed)

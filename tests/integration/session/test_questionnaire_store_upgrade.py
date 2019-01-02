from unittest.mock import patch, MagicMock

import simplejson as json

from app.data_model.questionnaire_store import QuestionnaireStore
from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.create_token import PAYLOAD


def get_mocked_questionnaire_store(data, version):
    """Returns a mocked version of the questionnaire storage, which allows
        injection of answers and older/invalid versions of the store.
    """

    # Add the default metadata
    metadata = dict(PAYLOAD)
    metadata.update(data['METADATA'])
    metadata['roles'] = ['dumper']  # Always give the dumper role
    data['METADATA'] = metadata

    json_data = json.dumps(data)
    mocked_store = MagicMock()
    mocked_store.get_user_data = MagicMock(return_value=(json_data, version))
    return patch('app.storage.encrypted_questionnaire_storage.EncryptedQuestionnaireStorage', return_value=mocked_store)


class TestLogin(IntegrationTestCase):

    def test_questionnaire_store_is_upgraded(self):
        # Given

        self.launchSurvey('test', 'numbers')

        # Increment the LATEST_VERSION so the `upgrade` method of answer_store is called when fetching
        # the questionnaire store.
        next_version = QuestionnaireStore.LATEST_VERSION + 1
        with patch('app.data_model.questionnaire_store.QuestionnaireStore.get_latest_version_number', return_value=next_version):
            with patch('app.data_model.questionnaire_store.AnswerStore.upgrade') as upgrade:
                self.post(action='start_questionnaire')

        upgrade.assert_called_once()

    def test_questionnaire_store_answer_store_group_instance_id_added(self):
        """ Simulates loading version 1 of an answer_store and seeing that it gets upgraded to version 2 """

        # Given
        existing_answers = [
            {
                'answer_id': 'primary-name',
                'answer_instance': 0,
                'group_instance': 0,
                'value': 'Han'
            },
            {
                'answer_id': 'repeating-anyone-else',
                'answer_instance': 0,
                'group_instance': 0,
                'value': 'Yes'
            },
            {
                'answer_id': 'repeating-name',
                'answer_instance': 0,
                'group_instance': 0,
                'value': 'Luke'
            },
            {
                'answer_id': 'repeating-anyone-else',
                'answer_instance': 0,
                'group_instance': 1,
                'value': 'Yes'
            },
            {
                'answer_id': 'repeating-name',
                'answer_instance': 0,
                'group_instance': 1,
                'value': 'Leia'
            },
            {
                'answer_id': 'repeating-anyone-else',
                'answer_instance': 0,
                'group_instance': 2,
                'value': 'No'
            }
        ]

        store_data = {
            'METADATA': {
                'eq_id': 'test',
                'form_type': 'routing_repeat_until',
                'tx_id': '0f6485e2-b9f1-439d-b90f-bd8a377a7d0b',
            },
            'ANSWERS': existing_answers,
            'COMPLETED_BLOCKS': [],
        }

        # When
        self.launchSurvey('test', 'routing_repeat_until', roles=['dumper'])

        with get_mocked_questionnaire_store(store_data, 1):
            dumped = self.dumpAnswers()

        answers = dumped['answers']

        for answer in answers:
            if answer['answer_id'] in ('primary-name', 'repeating-name'):
                # Then
                self.assertIsNotNone(
                    answer['group_instance_id']
                )

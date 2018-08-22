from unittest.mock import patch, MagicMock

import simplejson as json

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

        # Creates a QuestionnaireStore with a version of 0
        with patch('app.data_model.questionnaire_store.QuestionnaireStore.get_latest_version_number', return_value=0):
            self.launchSurvey('test', '0205')

        # LATEST_VERSION is now > 0 (it was 1 at time of writing), so the `upgrade` method
        # of answer_store should be called when fetching the questionnaire_store
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
                'answer_id': 'primary-anyone-else',
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
                'group_instance': 0,
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
                'group_instance': 1,
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

        # Then
        for i in answers:
            self.assertIn('group_instance_id', i)

        # This survey works out as having pairs of answers which should have
        # the same `group_instance_id`
        for i in range(0, 6, 2):
            self.assertEqual(
                answers[i]['group_instance_id'],
                answers[i+1]['group_instance_id']
            )

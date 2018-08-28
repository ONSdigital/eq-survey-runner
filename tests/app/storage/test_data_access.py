import mock

from app.data_model.app_models import QuestionnaireState
from app.storage import data_access
from tests.app.app_context_test_case import AppContextTestCase


USER_ID = 'someuser'
STATE_DATA = 'statedata'
VERSION = 1


class TestDataAccess(AppContextTestCase):

    def test_get_by_key(self):
        dynamo_item = QuestionnaireState(USER_ID, STATE_DATA, VERSION)

        with mock.patch('app.storage.dynamodb_api.get_by_key', return_value=dynamo_item) as get_by_key:
            model = data_access.get_by_key(QuestionnaireState, USER_ID)

        self.assertEqual(get_by_key.call_args[0][0], QuestionnaireState)
        self.assertEqual(get_by_key.call_args[0][1], USER_ID)

        self.assertEqual(model.user_id, USER_ID)
        self.assertEqual(model.state_data, STATE_DATA)
        self.assertEqual(model.version, VERSION)

    def test_put(self):
        model = QuestionnaireState(USER_ID, STATE_DATA, VERSION)

        with mock.patch('app.storage.dynamodb_api.put') as put:
            data_access.put(model)

        self.assertEqual(put.call_args[0][0], model)
        self.assertTrue(put.call_args[0][1])

    def test_delete(self):
        model = QuestionnaireState(USER_ID, STATE_DATA, VERSION)

        with mock.patch('app.storage.dynamodb_api.delete') as delete:
            data_access.delete(model)

        self.assertEqual(delete.call_args[0][0], model)

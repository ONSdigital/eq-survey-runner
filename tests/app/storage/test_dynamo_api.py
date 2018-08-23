from app.data_model.app_models import QuestionnaireState
from app.storage import dynamodb_api
from app.storage.errors import ItemAlreadyExistsError
from tests.app.app_context_test_case import AppContextTestCase


class TestDynamoApi(AppContextTestCase):

    def test_get_update(self):
        self._assert_item(None)
        _put_item(1)
        self._assert_item(1)
        _put_item(2)
        self._assert_item(2)

    def test_dont_overwrite(self):
        _put_item(1)
        with self.assertRaises(ItemAlreadyExistsError):
            _put_item(1, overwrite=False)

    def test_delete(self):
        _put_item(1)
        self._assert_item(1)
        model = QuestionnaireState('someuser', 'data', 1)
        dynamodb_api.delete(model)
        self._assert_item(None)

    def _assert_item(self, version):
        item = dynamodb_api.get_by_key(QuestionnaireState, 'someuser')
        actual_version = item.version if item else None
        self.assertEqual(actual_version, version)


def _put_item(version, overwrite=True):
    model = QuestionnaireState('someuser', 'data', version)
    dynamodb_api.put(model, overwrite)

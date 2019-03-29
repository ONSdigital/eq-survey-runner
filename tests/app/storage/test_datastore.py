import contextlib

import mock
from google.cloud import datastore as google_datastore

from tests.app.app_context_test_case import AppContextTestCase

from app.data_model.app_models import QuestionnaireState, QuestionnaireStateSchema
from app.storage.datastore import DatastoreStorage


class TestDatastore(AppContextTestCase):

    def setUp(self):
        super().setUp()

        self.mock_client = mock.Mock()
        self.mock_client.transaction.return_value = contextlib.suppress()
        self.ds = DatastoreStorage(self.mock_client)

    def test_get_by_key(self):
        model = QuestionnaireState('someuser', 'data', 1)
        model_data, _ = QuestionnaireStateSchema(strict=True).dump(model)

        m_entity = google_datastore.Entity()
        m_entity.update(model_data)
        self.mock_client.get.return_value = m_entity

        returned_model = self.ds.get_by_key(QuestionnaireState, 'someuser')

        self.assertEqual(model.user_id, returned_model.user_id)
        self.assertEqual(model.state_data, returned_model.state_data)
        self.assertEqual(model.version, returned_model.version)

    def test_get_not_found(self):
        self.mock_client.get.return_value = None
        returned_model = self.ds.get_by_key(QuestionnaireState, 'someuser')
        self.assertFalse(returned_model)

    def test_put(self):
        model = QuestionnaireState('someuser', 'data', 1)

        self.ds.put(model, True)

        put_data = self.mock_client.put.call_args[0][0]

        self.assertEqual(model.user_id, put_data['user_id'])
        self.assertEqual(model.state_data, put_data['state_data'])
        self.assertEqual(model.version, put_data['version'])

    def test_put_without_overwrite(self):
        model = QuestionnaireState('someuser', 'data', 1)

        with self.assertRaises(NotImplementedError) as exception:
            self.ds.put(model, False)

        self.assertEqual(exception.exception.args[0], 'Unique key checking not supported')

    def test_delete(self):
        model = QuestionnaireState('someuser', 'data', 1)
        self.ds.delete(model)

        self.assertEqual(self.mock_client.key.call_args[0][1], model.user_id)

        m_key = self.mock_client.key.return_value

        self.mock_client.delete.assert_called_once_with(m_key)

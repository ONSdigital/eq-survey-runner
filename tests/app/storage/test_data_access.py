import mock
from botocore.exceptions import ClientError
from sqlalchemy.exc import IntegrityError

from app.data_model import models
from app.data_model.app_models import QuestionnaireState, SubmittedResponse
from app.storage import data_access
from app.storage.data_access import ItemAlreadyExistsError
from tests.app.app_context_test_case import AppContextTestCase


USER_ID = 'someuser'
STATE_DATA = 'statedata'
VERSION = 1
COLLECTION_EXERCISE_ID = 'someid'
FORM_TYPE = 'someformtype'
RU_REF = 'someref'
EQ_ID = 'someid'



class TestDataAccess(AppContextTestCase):

    def test_get_by_key(self):
        dynamo_item = {'user_id': USER_ID, 'state_data': STATE_DATA, 'version': VERSION}

        with mock.patch('app.storage.dynamo_api.get_item', return_value=dynamo_item) as get_item:
            model = data_access.get_by_key(QuestionnaireState, USER_ID)

        self.assertEqual(get_item.call_args[0][1], {'user_id': USER_ID})

        self.assertEqual(model.user_id, USER_ID)
        self.assertEqual(model.state_data, STATE_DATA)
        self.assertEqual(model.version, VERSION)
        self.assertTrue(getattr(model, '_use_dynamo'))

    def test_get_by_key_rds_fallback(self):
        rds_model = models.QuestionnaireState(USER_ID, STATE_DATA, VERSION, COLLECTION_EXERCISE_ID, FORM_TYPE, RU_REF, EQ_ID)

        with mock.patch('app.storage.dynamo_api.get_item', return_value=None), \
             mock.patch.object(models.QuestionnaireState, 'query') as query:
            query.filter_by.return_value.first.return_value = rds_model
            model = data_access.get_by_key(QuestionnaireState, USER_ID)

        self.assertTrue(query.filter_by.return_value.first.called)

        self.assertEqual(model.user_id, USER_ID)
        self.assertEqual(model.state_data, STATE_DATA)
        self.assertEqual(model.version, VERSION)
        self.assertFalse(getattr(model, '_use_dynamo'))

    def test_by_key_no_sql(self):
        model = data_access.get_by_key(SubmittedResponse, USER_ID)

        self.assertIsNone(model)

    def test_put(self):
        model = QuestionnaireState(USER_ID, STATE_DATA, VERSION, COLLECTION_EXERCISE_ID, FORM_TYPE, RU_REF, EQ_ID)

        with mock.patch('app.storage.dynamo_api.put_item') as put_item:
            data_access.put(model)

        self.assertEqual(put_item.call_args[0][1], 'user_id')

        dynamo_item = put_item.call_args[0][2]
        self.assertEqual(dynamo_item['user_id'], USER_ID)
        self.assertEqual(dynamo_item['state_data'], STATE_DATA)
        self.assertEqual(dynamo_item['version'], VERSION)

        self.assertTrue(put_item.call_args[1]['overwrite'])

    def test_put_rds(self):
        model = QuestionnaireState(USER_ID, STATE_DATA, VERSION, COLLECTION_EXERCISE_ID, FORM_TYPE, RU_REF, EQ_ID)
        setattr(model, '_use_dynamo', False)

        with mock.patch('app.data_model.models.db.session.merge') as merge:
            data_access.put(model)

        self.assertTrue(merge.called)

        rds_model = merge.call_args[0][0]
        self.assertEqual(rds_model.user_id, USER_ID)
        self.assertEqual(rds_model.state, STATE_DATA)
        self.assertEqual(rds_model.version, VERSION)

    def test_put_no_overwrite(self):
        model = QuestionnaireState(USER_ID, STATE_DATA, VERSION, COLLECTION_EXERCISE_ID, FORM_TYPE, RU_REF, EQ_ID)

        side_effect = ClientError({'Error': {'Code': 'ConditionalCheckFailedException'}}, 'PutItem')
        with mock.patch('app.storage.dynamo_api.put_item', side_effect=side_effect) as put_item, \
            self.assertRaises(ItemAlreadyExistsError):
            data_access.put(model, overwrite=False)

        self.assertFalse(put_item.call_args[1]['overwrite'])

    def test_put_rds_no_overwrite(self):
        model = QuestionnaireState(USER_ID, STATE_DATA, VERSION, COLLECTION_EXERCISE_ID, FORM_TYPE, RU_REF, EQ_ID)
        setattr(model, '_use_dynamo', False)

        with mock.patch('app.data_model.models.db.session.add', side_effect=IntegrityError('', '', '')) as add, \
            self.assertRaises(ItemAlreadyExistsError):
            data_access.put(model, overwrite=False)

        self.assertTrue(add.called)

    def test_put_propogate_dynamo_exception(self):
        model = QuestionnaireState(USER_ID, STATE_DATA, VERSION, COLLECTION_EXERCISE_ID, FORM_TYPE, RU_REF, EQ_ID)

        side_effect = ClientError({'Error': {'Code': 'RandomError'}}, 'PutItem')
        with mock.patch('app.storage.dynamo_api.put_item', side_effect=side_effect) as put_item, \
            self.assertRaises(ClientError):
            data_access.put(model, overwrite=False)

        self.assertFalse(put_item.call_args[1]['overwrite'])

    def test_delete(self):
        model = QuestionnaireState(USER_ID, STATE_DATA, VERSION, COLLECTION_EXERCISE_ID, FORM_TYPE, RU_REF, EQ_ID)

        with mock.patch('app.storage.dynamo_api.delete_item') as delete_item:
            data_access.delete(model)

        self.assertEqual(delete_item.call_args[0][1], {'user_id': USER_ID})

    def test_delete_rds(self):
        model = QuestionnaireState(USER_ID, STATE_DATA, VERSION, COLLECTION_EXERCISE_ID, FORM_TYPE, RU_REF, EQ_ID)
        setattr(model, '_use_dynamo', False)

        with mock.patch('app.data_model.models.db.session.delete') as delete:
            data_access.delete(model)

        self.assertTrue(delete.called)

        rds_model = delete.call_args[0][0]
        self.assertEqual(rds_model.user_id, USER_ID)

    def test_dymo_no_write_when_read_disabled(self): # pylint: disable=no-self-use
        model = QuestionnaireState(USER_ID, STATE_DATA, VERSION, COLLECTION_EXERCISE_ID, FORM_TYPE, RU_REF, EQ_ID)
        with mock.patch('app.storage.data_access.is_dynamodb_read_enabled', mock.Mock(return_value=False)), \
                mock.patch('app.storage.data_access.models.db.session.add') as merge:
            data_access.put(model, overwrite=False)

        merge.assert_called()

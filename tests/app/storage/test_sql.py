import mock
from sqlalchemy.exc import IntegrityError

from tests.app.app_context_test_case import AppContextTestCase

from app.data_model import models
from app.data_model.app_models import QuestionnaireState
from app.storage.errors import ItemAlreadyExistsError
from app.storage.sql import SqlStorage

USER_ID = 'someuser'
STATE_DATA = 'statedata'
VERSION = 1


class TestSQL(AppContextTestCase):
    setting_overrides = {
        'EQ_STORAGE_BACKEND': 'sql',
        'SQLALCHEMY_DATABASE_URI': 'sqlite:////tmp/questionnaire.db',
    }

    def setUp(self):
        super().setUp()

        self.sql = SqlStorage()

    def test_get_by_key(self):
        rds_model = models.QuestionnaireState(USER_ID, STATE_DATA, VERSION)

        with mock.patch.object(models.QuestionnaireState, 'query') as query:
            query.filter_by.return_value.first.return_value = rds_model
            model = self.sql.get_by_key(QuestionnaireState, USER_ID)

        self.assertTrue(query.filter_by.return_value.first.called)

        self.assertEqual(model.user_id, USER_ID)
        self.assertEqual(model.state_data, STATE_DATA)
        self.assertEqual(model.version, VERSION)

    def test_put(self):
        model = QuestionnaireState(USER_ID, STATE_DATA, VERSION)

        with mock.patch('app.data_model.models.db.session.merge') as merge:
            self.sql.put(model, overwrite=True)

        self.assertTrue(merge.called)

        rds_model = merge.call_args[0][0]
        self.assertEqual(rds_model.user_id, USER_ID)
        self.assertEqual(rds_model.state, STATE_DATA)
        self.assertEqual(rds_model.version, VERSION)

    def test_put_no_overwrite(self):
        model = QuestionnaireState(USER_ID, STATE_DATA, VERSION)

        with mock.patch('app.data_model.models.db.session.add', side_effect=IntegrityError('', '', '')) as add, \
            self.assertRaises(ItemAlreadyExistsError):
            self.sql.put(model, overwrite=False)

        self.assertTrue(add.called)

    def test_delete(self):
        model = QuestionnaireState(USER_ID, STATE_DATA, VERSION)

        with mock.patch('app.data_model.models.db.session.delete') as delete:
            self.sql.delete(model)

        self.assertTrue(delete.called)

        rds_model = delete.call_args[0][0]
        self.assertEqual(rds_model.user_id, USER_ID)

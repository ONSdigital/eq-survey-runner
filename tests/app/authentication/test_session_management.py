from datetime import timedelta

from app.authentication.session_storage import SessionStorage
from tests.app.app_context_test_case import AppContextTestCase


class BaseSessionManagerTest(AppContextTestCase):
    def setUp(self):
        super().setUp()
        self._app.permanent_session_lifetime = timedelta(seconds=1)
        self.session_manager = SessionStorage()

    def test_has_token_empty(self):
        with self._app.test_request_context():
            self.assertIsNone(self.session_manager.get_user_id())

    def test_has_token(self):
        with self._app.test_request_context():
            self.session_manager.store_user_id('test')
            self.assertIsNotNone(self.session_manager.get_user_id())

    def test_remove_token(self):
        with self._app.test_request_context():
            self.session_manager.store_user_id('test')
            self.assertIsNotNone(self.session_manager.get_user_id())
            self.session_manager.delete_session_from_db()
            self.assertIsNone(self.session_manager.get_user_id())

    def test_remove_user_ik(self):
        with self._app.test_request_context():
            self.session_manager.remove_user_ik()
            self.assertIsNone(self.session_manager.get_user_ik())

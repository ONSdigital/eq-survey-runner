from app.navigation.navigation_store import NavigationStore
from app.navigation.navigation_state import NavigationState
from tests.app.framework.sr_unittest import SurveyRunnerTestCase
import unittest


class FlaskNavigationStoreTest(SurveyRunnerTestCase):

    def test_add_history(self):
        with self.application.test_request_context():
            navigation_store = NavigationStore()
            navigation_state = NavigationState()
            navigation_state.current_position = "start"
            navigation_store.store_state(navigation_state)
            self.assertEquals("start", navigation_store.get_state().current_position)

if __name__ == '__main__':
    unittest.main()

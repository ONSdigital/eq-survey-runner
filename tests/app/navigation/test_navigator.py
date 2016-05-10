from app.navigation.navigator import Navigator
from app.navigation.navigation_history import FlaskNavigationHistory
from tests.app.framework.sr_unittest import SurveyRunnerTestCase
from app.model.questionnaire import Questionnaire
import unittest


class NavigatorTest(SurveyRunnerTestCase):

    def test_get_current_location(self):
        with self.application.test_request_context():
            schema = Questionnaire()

            navigation_history = FlaskNavigationHistory()
            navigator = Navigator(schema, navigation_history)
            #  brand new session shouldn't have a current location
            self.assertEquals("questionnaire", navigator.get_current_location())

    def test_get_current_location_with_intro(self):
        with self.application.test_request_context():
            schema = Questionnaire()
            schema.introduction = "anything"

            navigation_history = FlaskNavigationHistory()
            navigator = Navigator(schema, navigation_history)
            #  brand new session shouldn't have a current location
            self.assertEquals("introduction", navigator.get_current_location())

    def test_go_to(self):
        with self.application.test_request_context():
            schema = Questionnaire()

            navigation_history = FlaskNavigationHistory()
            navigator = Navigator(schema, navigation_history)
            navigator.go_to("completed")
            self.assertEquals("completed", navigator.get_current_location())

if __name__ == '__main__':
    unittest.main()

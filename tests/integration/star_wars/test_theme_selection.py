from .star_wars_tests import StarWarsTestCase


class TestThemeSelection(StarWarsTestCase):
    """
    This test checks that we are using the Star wars theme as
    specified in the test survey schema.
    """

    def test_theme(self):
        self.launchSurvey()

        self.start_questionnaire_and_navigate_routing()

        # We are in the Questionnaire
        self.assertInPage('Theme selected: Star Wars')

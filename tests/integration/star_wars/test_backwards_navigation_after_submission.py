from tests.integration.star_wars import star_wars_test_urls, BLOCK_2_DEFAULT_ANSWERS, BLOCK_7_DEFAULT_ANSWERS, \
    BLOCK_8_DEFAULT_ANSWERS
from .star_wars_tests import StarWarsTestCase


class TestBackwardsNavigationAfterSubmission(StarWarsTestCase):

    def test_backwards_navigation_star_wars(self):
        # submit a survey
        self.launchSurvey()
        self.start_questionnaire_and_navigate_routing()
        self.post(BLOCK_2_DEFAULT_ANSWERS)
        self.post(BLOCK_7_DEFAULT_ANSWERS)
        self.post(BLOCK_8_DEFAULT_ANSWERS)
        self.post(action=None)
        self.assertInUrl('thank-you')

        # Now try going back into the survey
        self.backwards_navigation()

    def backwards_navigation(self):
        # Introduction
        self.get(star_wars_test_urls.STAR_WARS_INTRODUCTION)
        self.assertStatusUnauthorised()

        # Block Three
        self.get(star_wars_test_urls.STAR_WARS_QUIZ_3)
        self.assertStatusUnauthorised()

        # Block Two
        self.get(star_wars_test_urls.STAR_WARS_QUIZ_2)
        self.assertStatusUnauthorised()

        # Block One
        self.get(star_wars_test_urls.STAR_WARS_QUIZ_1)
        self.assertStatusUnauthorised()

        # Introduction
        self.get(star_wars_test_urls.STAR_WARS_INTRODUCTION)
        self.assertStatusUnauthorised()

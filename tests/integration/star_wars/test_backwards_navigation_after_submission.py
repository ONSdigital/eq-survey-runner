from tests.integration.star_wars import star_wars_test_urls, \
    STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS, \
    STAR_WARS_TRIVIA_PART_2_DEFAULT_ANSWERS, \
    STAR_WARS_TRIVIA_PART_3_DEFAULT_ANSWERS
from .star_wars_tests import StarWarsTestCase


class TestBackwardsNavigationAfterSubmission(StarWarsTestCase):

    def test_backwards_navigation_star_wars(self):
        # submit a survey
        self.launchSurvey()
        self.start_questionnaire_and_navigate_routing()
        self.post(STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS)
        self.post(STAR_WARS_TRIVIA_PART_2_DEFAULT_ANSWERS)
        self.post(STAR_WARS_TRIVIA_PART_3_DEFAULT_ANSWERS)
        self.post(action=None)
        self.assertInUrl('thank-you')

        # Now try going back into the survey
        self.backwards_navigation()

    def backwards_navigation(self):

        # Block Three
        self.get(star_wars_test_urls.STAR_WARS_TRIVIA_PART_3)
        self.assertStatusUnauthorised()

        # Block Two
        self.get(star_wars_test_urls.STAR_WARS_TRIVIA_PART_2)
        self.assertStatusUnauthorised()

        # Block One
        self.get(star_wars_test_urls.STAR_WARS_TRIVIA_PART_1)
        self.assertStatusUnauthorised()

        # Introduction
        self.get(star_wars_test_urls.STAR_WARS_INTRODUCTION)
        self.assertStatusUnauthorised()

from tests.integration.star_wars import star_wars_test_urls, \
    STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS, \
    STAR_WARS_TRIVIA_PART_2_DEFAULT_ANSWERS, \
    STAR_WARS_TRIVIA_PART_3_DEFAULT_ANSWERS
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestEmptySubmissionFails(StarWarsTestCase):

    def test_empty_submission_fails(self):
        self.launchSurvey()

        # go to the first page
        self.start_questionnaire_and_navigate_routing()

        # now issue a request to the summary page
        self.get(star_wars_test_urls.STAR_WARS_SUMMARY)

        # check that we're redirected to the first block as its an empty submission
        self.assertInUrl(star_wars_test_urls.STAR_WARS_TRIVIA_PART_1)

        # Form submission with no errors
        self.post(STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS)
        self.assertInUrl('star-wars-trivia-part-2')

        # Second page
        # Pipe Test for section title
        self.assertInPage('On 2 June 1983 how many were employed?')

        # Textarea question
        self.assertInPage('Why doesn\'t Chewbacca receive a medal at the end of A New Hope?')
        self.assertInPage('chewbacca-medal-answer')

        self.post(STAR_WARS_TRIVIA_PART_2_DEFAULT_ANSWERS)

        # third page
        self.assertInPage("Finally, which  is your favourite film?")
        self.post(STAR_WARS_TRIVIA_PART_3_DEFAULT_ANSWERS)

        # There are no validation errors
        self.assertRegexUrl(star_wars_test_urls.STAR_WARS_SUMMARY_REGEX)

        # We are on the review answers page
        self.assertInPage('>Star Wars</')
        self.assertInPage('>Your responses<')
        self.assertRegexPage('(?s)How old is Chewy?.*?234')
        self.assertRegexPage('(?s)How many Octillions do Nasa reckon it would cost to build a death star?.*?£40')
        self.assertRegexPage('(?s)How hot is a lightsaber in degrees C?.*?1370')
        self.assertRegexPage('(?s)What animal was used to create the engine sound of the Empire\'s TIE fighters?.*?Elephant')
        self.assertRegexPage('(?s)Which of these Darth Vader quotes is wrong?.*?Luke, I am your father')
        self.assertRegexPage('(?s)Which 3 have wielded a green lightsaber?.*?Yoda')
        self.assertRegexPage('(?s)Which 3 have wielded a green lightsaber?.*?Luke Skywalker')
        self.assertRegexPage('(?s)Which 3 have wielded a green lightsaber?.*?Qui-Gon Jinn')
        self.assertRegexPage('(?s)Which 3 appear in any of the opening crawlers?')
        self.assertRegexPage('(?s)When was The Empire Strikes Back released?.*?28 May 1983 to 29 May 1983')
        self.assertRegexPage('(?s)What was the total number of Ewoks?.*?')
        self.assertRegexPage('(?s)Why doesn\'t Chewbacca receive a medal at the end of A New Hope?.*?'
                             'Wookiees don’t place value in material rewards and refused the medal initially')
        self.assertInPage('>Please check your responses carefully before submitting.<')
        self.assertInPage('>Submit answers<')

        # Submit answers
        self.post(action=None)
        self.assertInUrl('thank-you')

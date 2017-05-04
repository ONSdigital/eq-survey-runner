from tests.integration.star_wars import star_wars_test_urls, \
    STAR_WARS_TRIVIA_PART_2_DEFAULT_ANSWERS, \
    STAR_WARS_TRIVIA_PART_3_DEFAULT_ANSWERS, \
    STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestNavigation(StarWarsTestCase):

    def test_light_side_path(self):
        self.launchSurvey()

        self.start_questionnaire_and_navigate_routing()

        # navigate back to the introduction
        self.get(star_wars_test_urls.STAR_WARS_INTRODUCTION)

        # navigate to the first page
        self.get(star_wars_test_urls.STAR_WARS_TRIVIA_PART_1)

        # Form submission with no errors
        self.post(STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS)

        # Check the second page (we're on it already)
        self.assertInUrl('star-wars-trivia-part-2')
        self.check_second_quiz_page()

        # now navigate back to the first page
        self.get(star_wars_test_urls.STAR_WARS_TRIVIA_PART_1)
        self._check_quiz_first_page()

        # now go back to the second page
        self.get(star_wars_test_urls.STAR_WARS_TRIVIA_PART_2)
        self.check_second_quiz_page()

        # And continue
        self.assertInUrl('star-wars-trivia-part-2')
        self.post(STAR_WARS_TRIVIA_PART_2_DEFAULT_ANSWERS)

        # third page
        self.assertInUrl('star-wars-trivia-part-3')
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
        self.assertRegexPage('(?s)What animal was used to create the engine sound of the Empire\'s TIE fighters?.*?Elephant')  # NOQA
        self.assertRegexPage('(?s)Which of these Darth Vader quotes is wrong?.*?Luke, I am your father')
        self.assertRegexPage('(?s)Which 3 have wielded a green lightsaber?.*?Yoda')  # NOQA
        self.assertRegexPage('(?s)Which 3 appear in any of the opening crawlers?')
        self.assertRegexPage('(?s)When was The Empire Strikes Back released?.*?28 May 1983 to 29 May 1983')  # NOQA
        self.assertRegexPage('(?s)What was the total number of Ewoks?.*?')
        self.assertRegexPage('(?s)Why doesn\'t Chewbacca receive a medal at the end of A New Hope?.*?'
                             'Wookiees don’t place value in material rewards and refused the medal initially')  # NOQA
        self.assertInPage('>Please check your responses carefully before submitting.<')
        self.assertInPage('>Submit answers<')

        # Submit answers
        self.post(action=None)
        self.assertInUrl('thank-you')

    def _check_quiz_first_page(self):
        self.assertInPage(">Save and continue<")
        self.assertInPage('Star Wars Quiz')
        self.assertInPage('May the force be with you young EQ developer')

        # Integer question
        self.assertInPage('How old is Chewy?')
        self.assertInPage('chewies-age-answer')

        # Currency question
        self.assertInPage('How many Octillions do Nasa reckon it would cost to build a death star?')
        self.assertInPage('death-star-cost-answer')

        # Radio box question
        self.assertInPage('What animal was used to create the engine sound of the Empire\'s TIE fighters?')  # NOQA
        self.assertInPage('Lion')
        self.assertInPage('Cow')
        self.assertInPage('Elephant')
        self.assertInPage('Hippo')
        self.assertInPage('tie-fighter-sound-answer')

        # Checkbox question
        self.assertInPage('Which 3 have wielded a green lightsaber?')
        self.assertInPage('Luke Skywalker')
        self.assertInPage('Anakin Skywalker')
        self.assertInPage('Obi-Wan Kenobi')
        self.assertInPage('Yoda')
        self.assertInPage('Rey')
        self.assertInPage('Qui-Gon Jinn')
        self.assertInPage('green-lightsaber-answer')

        # Date Range question
        self.assertInPage('When was The Empire Strikes Back released?')
        self.assertInPage('Period from')
        self.assertInPage('Period to')
        self.assertInPage('Day')
        self.assertInPage('Month')
        self.assertInPage('Year')
        self.assertInPage('empire-strikes-back-from-answer')
        self.assertInPage('empire-strikes-back-to-answer')

        # Pipe Test for question description
        self.assertInPage('It could be between 1 April 2016 and 30 April 2016. But that might just be a test')  # NOQA

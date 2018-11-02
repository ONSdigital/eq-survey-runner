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
        self.assertInBody('Finally, which  is your favourite film?')
        self.post(STAR_WARS_TRIVIA_PART_3_DEFAULT_ANSWERS)

        # There are no validation errors
        self.assertRegexUrl(star_wars_test_urls.STAR_WARS_SUMMARY_REGEX)

        # We are on the review answers page
        self.assertInBody('>Star Wars</')
        self.assertInBody('>Check your answers and submit<')
        self.assertRegexPage('(?s)How old is Chewy?.*?234')
        self.assertRegexPage('(?s)How many Octillions do Nasa reckon it would cost to build a death star?.*?£40')
        self.assertRegexPage('(?s)How hot is a lightsaber in degrees C?.*?1,370')
        self.assertRegexPage("(?s)What animal was used to create the engine sound of the Empire's TIE fighters?.*?Elephant")  # NOQA
        self.assertRegexPage('(?s)Which of these Darth Vader quotes is wrong?.*?Luke, I am your father')
        self.assertRegexPage('(?s)Which 3 have wielded a green lightsaber?.*?Yoda')  # NOQA
        self.assertRegexPage('(?s)Which 3 appear in any of the opening crawlers?')
        self.assertRegexPage("(?s)When was The Empire Strikes Back released?.*?<span class='date'>28 May 1983</span> "
                             "to <span class='date'>29 May 1983</span>")  # NOQA
        self.assertRegexPage('(?s)What was the total number of Ewoks?.*?')
        self.assertRegexPage("(?s)Why doesn't Chewbacca receive a medal at the end of A New Hope?.*?"
                             'Wookiees don’t place value in material rewards and refused the medal initially')  # NOQA
        self.assertInBody('>You can check your answers below<')
        self.assertInBody('>Submit answers<')

        # Submit answers
        self.post(action=None)
        self.assertInUrl('thank-you')

    def _check_quiz_first_page(self):
        self.assertInBody('>Save and continue<')
        self.assertInBody('Star Wars Quiz')
        self.assertInBody('May the force be with you young EQ developer')

        # Integer question
        self.assertInBody('How old is Chewy?')
        self.assertInBody('chewies-age-answer')

        # Currency question
        self.assertInBody('How many Octillions do Nasa reckon it would cost to build a death star?')
        self.assertInBody('death-star-cost-answer')

        # Radio box question
        self.assertInBody("What animal was used to create the engine sound of the Empire's TIE fighters?")  # NOQA
        self.assertInBody('Lion')
        self.assertInBody('Cow')
        self.assertInBody('Elephant')
        self.assertInBody('Hippo')
        self.assertInBody('tie-fighter-sound-answer')

        # Checkbox question
        self.assertInBody('Which 3 have wielded a green lightsaber?')
        self.assertInBody('Luke Skywalker')
        self.assertInBody('Anakin Skywalker')
        self.assertInBody('Obi-Wan Kenobi')
        self.assertInBody('Yoda')
        self.assertInBody('Rey')
        self.assertInBody('Qui-Gon Jinn')
        self.assertInBody('green-lightsaber-answer')

        # Date Range question
        self.assertInBody('When was The Empire Strikes Back released?')
        self.assertInBody('Period from')
        self.assertInBody('Period to')
        self.assertInBody('Day')
        self.assertInBody('Month')
        self.assertInBody('Year')
        self.assertInBody('empire-strikes-back-from-answer')
        self.assertInBody('empire-strikes-back-to-answer')

        # Pipe Test for question description
        self.assertInBody('It could be between <span class="date">1 April 2016</span> and '
                          '<span class="date">30 April 2016</span>. But that might just be a test')  # NOQA

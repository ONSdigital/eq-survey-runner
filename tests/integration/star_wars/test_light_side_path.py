from tests.integration.star_wars import star_wars_test_urls, \
    STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS, \
    STAR_WARS_TRIVIA_PART_2_DEFAULT_ANSWERS, \
    STAR_WARS_TRIVIA_PART_3_DEFAULT_ANSWERS
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestLightSidePath(StarWarsTestCase):

    def test_light_side_path(self):
        self.launchSurvey()

        self.start_questionnaire_and_navigate_routing()

        # Form submission with no errors
        self.post(STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS)

        # Second page
        self.assertInUrl('star-wars-trivia-part-2')

        # Pipe Test for section title
        self.assertInBody('On <span class="date">2 June 1983</span> how many were employed?')

        # Textarea question
        self.assertInBody("Why doesn't Chewbacca receive a medal at the end of A New Hope?")
        self.assertInBody('chewbacca-medal-answer')

        self.post(STAR_WARS_TRIVIA_PART_2_DEFAULT_ANSWERS)

        # third page
        self.assertInBody('Finally, which  is your favourite film?')

        self.post(STAR_WARS_TRIVIA_PART_3_DEFAULT_ANSWERS)

        # There are no validation errors
        self.assertInUrl(star_wars_test_urls.STAR_WARS_SUMMARY)

        # We are on the review answers page
        self.assertInBody('>Star Wars</')
        self.assertInBody('>Check your answers and submit<')
        self.assertRegexPage('(?s)How old is Chewy?.*?234')
        self.assertRegexPage('(?s)How many Octillions do Nasa reckon it would cost to build a death star?.*?£40')
        self.assertRegexPage('(?s)How hot is a lightsaber in degrees C?.*?1,370')
        self.assertRegexPage("(?s)What animal was used to create the engine sound of the Empire's TIE fighters?.*?Elephant")
        self.assertRegexPage('(?s)Which of these Darth Vader quotes is wrong?.*?Luke, I am your father')
        self.assertRegexPage('(?s)Which 3 have wielded a green lightsaber?.*?Yoda')
        self.assertRegexPage('(?s)Which 3 have wielded a green lightsaber?.*?Luke Skywalker')
        self.assertRegexPage('(?s)Which 3 have wielded a green lightsaber?.*?Qui-Gon Jinn')
        self.assertRegexPage('(?s)Which 3 appear in any of the opening crawlers?')
        self.assertRegexPage('(?s)When was The Empire Strikes Back released?.*?28 May 1983.*?to.*?29 May 1983')
        self.assertRegexPage('(?s)What was the total number of Ewoks?.*?')
        self.assertRegexPage("(?s)Why doesn't Chewbacca receive a medal at the end of A New Hope?.*?"
                             'Wookiees don’t place value in material rewards and refused the medal initially')
        self.assertInBody('You can check your answers below')
        self.assertInBody('>Submit answers<')

        # Post answers
        self.post(action=None)
        self.assertInUrl('thank-you')

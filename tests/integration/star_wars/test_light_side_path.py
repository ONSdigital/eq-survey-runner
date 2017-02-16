from tests.integration.star_wars import star_wars_test_urls, BLOCK_2_DEFAULT_ANSWERS, BLOCK_7_DEFAULT_ANSWERS, \
    BLOCK_8_DEFAULT_ANSWERS
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestLightSidePath(StarWarsTestCase):

    def test_light_side_path(self):

        self.login()

        first_page = self.start_questionnaire_and_navigate_routing()

        # Form submission with no errors
        resp = self.submit_page(first_page, BLOCK_2_DEFAULT_ANSWERS)
        self.assertNotEqual(resp.location, first_page)

        # Second page
        second_page = resp.location
        resp = self.navigate_to_page(second_page)
        content = resp.get_data(True)

        # Pipe Test for section title
        self.assertRegex(content, 'On 2 June 1983 how many were employed?')

        # Textarea question
        self.assertRegex(content, 'Why doesn\'t Chewbacca receive a medal at the end of A New Hope?')
        self.assertRegex(content, '215015b1-f87c-4740-9fd4-f01f707ef558')

        resp = self.submit_page(second_page, BLOCK_7_DEFAULT_ANSWERS)

        # third page
        third_page = resp.location
        resp = self.navigate_to_page(third_page)
        content = resp.get_data(True)

        self.assertRegex(content, "Finally, which  is your favourite film?")

        resp = self.submit_page(third_page, BLOCK_8_DEFAULT_ANSWERS)

        # There are no validation errors
        self.assertRegex(resp.location, star_wars_test_urls.STAR_WARS_SUMMARY)

        summary_url = resp.location

        resp = self.navigate_to_page(summary_url)

        # We are on the review answers page
        content = resp.get_data(True)
        self.assertRegex(content, '<title>Summary</title>')
        self.assertRegex(content, '>Star Wars</')
        self.assertRegex(content, '>Your responses<')
        self.assertRegex(content, '(?s)How old is Chewy?.*?234')
        self.assertRegex(content, '(?s)How many Octillions do Nasa reckon it would cost to build a death star?.*?£40')
        self.assertRegex(content, '(?s)How hot is a lightsaber in degrees C?.*?1370')
        self.assertRegex(content, '(?s)What animal was used to create the engine sound of the Empire\'s TIE fighters?.*?Elephant')  # NOQA
        self.assertRegex(content, '(?s)Which of these Darth Vader quotes is wrong?.*?Luke, I am your father')
        self.assertRegex(content, '(?s)Which 3 have wielded a green lightsaber?.*?Yoda')  # NOQA
        self.assertRegex(content, '(?s)Which 3 have wielded a green lightsaber?.*?Luke Skywalker')  # NOQA
        self.assertRegex(content, '(?s)Which 3 have wielded a green lightsaber?.*?Qui-Gon Jinn')  # NOQA
        self.assertRegex(content, '(?s)Which 3 appear in any of the opening crawlers?')
        self.assertRegex(content, '(?s)When was The Empire Strikes Back released?.*?28 May 1983 to 29 May 1983')  # NOQA
        self.assertRegex(content, '(?s)What was the total number of Ewoks?.*?')
        self.assertRegex(content, '(?s)Why doesn\'t Chewbacca receive a medal at the end of A New Hope?.*?'
                                  'Wookiees don’t place value in material rewards and refused the medal initially')  # NOQA
        self.assertRegex(content, 'Please check carefully before submission')
        self.assertRegex(content, '>Submit answers<')

        self.complete_survey('star_wars')

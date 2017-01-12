from tests.integration.star_wars import star_wars_test_urls, BLOCK_7_DEFAULT_ANSWERS, BLOCK_8_DEFAULT_ANSWERS, \
    BLOCK_2_DEFAULT_ANSWERS
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestNavigation(StarWarsTestCase):

    def test_light_side_path(self):

        self.login_and_check_introduction_text()

        first_page = self.start_questionnaire_and_navigate_routing()

        introduction = star_wars_test_urls.STAR_WARS_INTRODUCTION

        resp = self.navigate_to_page(introduction)

        self.check_introduction_text(resp)

        # navigate back to first page
        self.navigate_to_page(first_page)

        # Form submission with no errors
        resp = self.submit_page(first_page, BLOCK_2_DEFAULT_ANSWERS)
        self.assertNotEqual(resp.location, first_page)

        second_page = resp.location

        # go to the second page
        self.check_second_quiz_page(second_page)

        # now navigate back to the first page
        self.check_quiz_first_page(first_page)

        # now go back to the second page
        self.check_second_quiz_page(second_page)

        resp = self.submit_page(second_page, BLOCK_7_DEFAULT_ANSWERS)

        # third page
        third_page = resp.location
        resp = self.navigate_to_page(third_page)
        content = resp.get_data(True)

        self.assertRegex(content, "Finally, which  is your favourite film?")

        resp = self.submit_page(third_page, BLOCK_8_DEFAULT_ANSWERS)

        # There are no validation errors
        self.assertRegex(resp.location, star_wars_test_urls.STAR_WARS_SUMMARY_REGEX)

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
        self.assertRegex(content, '(?s)Which 3 appear in any of the opening crawlers?')
        self.assertRegex(content, '(?s)When was The Empire Strikes Back released?.*?28 May 1983 to 29 May 1983')  # NOQA
        self.assertRegex(content, '(?s)What was the total number of Ewokes?.*?')
        self.assertRegex(content, '(?s)Why doesn\'t Chewbacca receive a medal at the end of A New Hope?.*?'
                                  'Wookiees don’t place value in material rewards and refused the medal initially')  # NOQA
        self.assertRegex(content, '>Please check carefully before submission.<')
        self.assertRegex(content, '>Submit answers<')

        self.complete_survey(summary_url, 'star_wars')

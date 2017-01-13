from tests.integration.star_wars import star_wars_test_urls, BLOCK_7_DEFAULT_ANSWERS, BLOCK_8_DEFAULT_ANSWERS, \
    BLOCK_2_DEFAULT_ANSWERS
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestNavigation(StarWarsTestCase):

    def test_light_side_path(self):

        self.login()

        first_page = self.start_questionnaire_and_navigate_routing()

        introduction = star_wars_test_urls.STAR_WARS_INTRODUCTION

        resp = self.navigate_to_page(introduction)

        # navigate back to first page
        self.navigate_to_page(first_page)

        # Form submission with no errors
        resp = self.submit_page(first_page, BLOCK_2_DEFAULT_ANSWERS)
        self.assertNotEqual(resp.location, first_page)

        second_page = resp.location

        # go to the second page
        self.check_second_quiz_page(second_page)

        # now navigate back to the first page
        self._check_quiz_first_page(first_page)

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

    def _check_quiz_first_page(self, page):
        content = self.retrieve_content(page)
        self.assertIn(">Save and continue<", content)
        self.assertIn('Star Wars Quiz', content)
        self.assertIn('May the force be with you young EQ developer', content)

        # Integer question
        self.assertIn('How old is Chewy?', content)
        self.assertIn('6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b', content)

        # Currency question
        self.assertIn('How many Octillions do Nasa reckon it would cost to build a death star?', content)
        self.assertIn('92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c', content)

        # Radio box question
        self.assertIn('What animal was used to create the engine sound of the Empire&#39;s TIE fighters?', content)  # NOQA
        self.assertIn('Lion', content)
        self.assertIn('Cow', content)
        self.assertIn('Elephant', content)
        self.assertIn('Hippo', content)
        self.assertIn('a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d', content)

        # Checkbox question
        self.assertIn('Which 3 have wielded a green lightsaber?', content)
        self.assertIn('Luke Skywalker', content)
        self.assertIn('Anakin Skywalker', content)
        self.assertIn('Obi-Wan Kenobi', content)
        self.assertIn('Yoda', content)
        self.assertIn('Rey', content)
        self.assertIn('Qui-Gon Jinn', content)
        self.assertIn('9587eb9b-f24e-4dc0-ac94-66117b896c10', content)

        # Date Range question
        self.assertIn('When was The Empire Strikes Back released?', content)
        self.assertIn('Period from', content)
        self.assertIn('Period to', content)
        self.assertIn('Day', content)
        self.assertIn('Month', content)
        self.assertIn('Year', content)
        self.assertIn('6fd644b0-798e-4a58-a393-a438b32fe637', content)
        self.assertIn('06a6a4b7-6ce4-4687-879d-3443cd8e2ff0', content)

        # Pipe Test for question description
        self.assertIn('It could be between 1 April 2016 and 30 April 2016. But that might just be a test', content)  # NOQA

        return page

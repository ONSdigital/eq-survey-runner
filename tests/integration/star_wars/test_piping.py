from tests.integration.star_wars import BLOCK_2_DEFAULT_ANSWERS
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestPiping(StarWarsTestCase):

    def test_piping_employment_date(self):
        self.login()

        first_page = self.start_questionnaire_and_navigate_routing()

        # We submit the form
        resp = self.submit_page(first_page, BLOCK_2_DEFAULT_ANSWERS)

        # On to page two
        second_page = resp.location

        resp = self.navigate_to_page(second_page)

        # We are in the Questionnaire
        content = resp.get_data(True)

        self.assertRegex(content, 'On 2 June 1983 how many were employed?')

    def test_piping_an_answer(self):
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

        # Check Cheewies Age has been correctly piped into the question text
        self.assertRegex(content, "Do you really think that Chewbacca is 234 years old?")

from tests.integration.star_wars import star_wars_test_urls, BLOCK_2_DEFAULT_ANSWERS
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestEmptyRadioBoxes(StarWarsTestCase):

    def test_radio_boxes_mandatory_empty(self):

        self.login()

        first_page = self.start_questionnaire_and_navigate_routing()

        # We fill in the survey without a mandatory radio box

        # We fill in our answers missing one required field
        form_data = BLOCK_2_DEFAULT_ANSWERS.copy()
        del form_data['a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d']

        # We submit the form
        resp = self.submit_page(first_page, form_data)

        # We stay on the current page
        content = resp.get_data(True)
        self.assertRegex(content, 'Star Wars Quiz')
        self.assertRegex(content, 'May the force be with you young EQ developer')
        self.assertRegex(content, 'This page has 1 errors')
        self.assertRegex(content, 'This field is mandatory.')

        # We submit the form
        resp = self.submit_page(first_page, BLOCK_2_DEFAULT_ANSWERS)

        # There are no validation errors
        self.assertRegex(resp.location, star_wars_test_urls.STAR_WARS_QUIZ_2)
        summary_url = resp.location
        resp = self.navigate_to_page(summary_url)

        # Check we are on the next page
        content = resp.get_data(True)
        self.assertRegex(content, 'Why doesn\'t Chewbacca receive a medal at the end of A New Hope?')

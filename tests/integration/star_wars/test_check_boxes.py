from tests.integration.star_wars import star_wars_test_urls, BLOCK_2_DEFAULT_ANSWERS
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestEmptyCheckBoxes(StarWarsTestCase):

    def test_check_boxes_mandatory_empty(self):
        self.login()

        first_page = self.start_questionnaire_and_navigate_routing()

        # We fill in the survey without a mandatory check box
        form_data = BLOCK_2_DEFAULT_ANSWERS.copy()
        # Skip this question
        del form_data['9587eb9b-f24e-4dc0-ac94-66117b896c10']

        # We submit the form
        resp = self.submit_page(first_page, form_data)

        # We stay on the current page
        content = resp.get_data(True)
        self.assertIn('Star Wars Quiz', content)
        self.assertIn('May the force be with you young EQ developer', content)
        self.assertIn('This page has 1 errors', content)
        self.assertIn('This field is mandatory.', content)

        # We correct the error
        resp = self.submit_page(first_page, BLOCK_2_DEFAULT_ANSWERS)

        # There are no validation errors

        self.assertIn(star_wars_test_urls.STAR_WARS_QUIZ_2, resp.location)
        second_page = resp.location

        self.check_second_quiz_page(second_page)

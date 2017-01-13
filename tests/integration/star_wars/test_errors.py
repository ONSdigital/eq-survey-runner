from tests.integration.create_token import create_token
from tests.integration.star_wars import BLOCK_2_DEFAULT_ANSWERS
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestPageErrors(StarWarsTestCase):
    def test_multi_page_errors(self):
        # Get a token
        self.login()

        first_page = self.start_questionnaire_and_navigate_routing()

        resp = self.submit_page(first_page, BLOCK_2_DEFAULT_ANSWERS)

        self.assertNotEqual(resp.location, first_page)
        # Second page
        second_page = resp.location

        self.check_second_quiz_page(second_page)

        # Our answers
        form_data = {
            # Make this data missing
            "215015b1-f87c-4740-9fd4-f01f707ef558": "",  # Required answer
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        self.submit_page(second_page, form_data)

        # We fill in our answers missing one required field
        form_data = BLOCK_2_DEFAULT_ANSWERS.copy()
        del form_data['a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d']

        # We submit the form
        resp = self.submit_page(first_page, form_data)

        content = resp.get_data(True)
        self.assertRegex(content, 'href="#a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d"')
        # We DO NOT have the error from page two
        self.assertNotRegex(content, 'href="215015b1-f87c-4740-9fd4-f01f707ef558"')

    def test_skip_question_errors(self):
        # Given on the page with skip question with skip condition
        token = create_token('skip_condition', 'test')
        self.client.get('/session?token=' + token.decode(), follow_redirects=True)
        post_data = {'action[start_questionnaire]': 'Start Questionnaire'}
        self.client.post('/questionnaire/test/skip_condition/201604/789/introduction', data=post_data, follow_redirects=True)
        post_data = {'food-answer': 'Bacon', 'action[save_continue]': 'Save &amp; Continue'}
        self.client.post('/questionnaire/test/skip_condition/201604/789/breakfast/0/food-block', data=post_data, follow_redirects=True)

        # When submit no answers which is invalid
        post_data = {'action[save_continue]': 'Save &amp; Continue'}
        resp = self.client.post('/questionnaire/test/skip_condition/789/breakfast/0/drink-block', data=post_data)

        # Then errors exists on page
        self.assertEqual(resp.status_code, 200)
        self.assertRegex(resp.get_data(True), 'This page has 1 errors')

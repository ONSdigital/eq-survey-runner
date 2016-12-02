from werkzeug.datastructures import MultiDict

from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


class TestHouseholdQuestion(IntegrationTestCase):

    INTRODUCTION_PAGE = '/questionnaire/test/household_question/789/introduction'

    def setUp(self):
        super(TestHouseholdQuestion, self).setUp()

    def tearDown(self):
        super(TestHouseholdQuestion, self).tearDown()

    def test_add_answer(self):
        self.add_answers()

    def test_remove_answer(self):
        first_page = self.add_answers()
        self.remove_answer(first_page)

    def test_regular_submit(self):
        first_page = self.add_answers()
        self.submit_answers(first_page)

    def submit_answers(self, page):
        # Add first person
        form_data = MultiDict()
        form_data.add("first-name", 'Person One')
        form_data.add("first-name_1", 'Person Two')
        form_data.add("first-name_2", 'Person Three')
        form_data.add("first-name_3", 'Person Four')
        form_data.add("action[save_continue]", "") # Remove person two.
        resp = self.client.post(page, data=form_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        summary_page = resp.headers['Location']
        self.assertNotEqual(page, summary_page)

        resp = self.navigate_to_page(summary_page)
        content = resp.get_data(True)

        self.assertRegex(content, 'Your responses')
        self.assertRegex(content, 'Person One')
        self.assertRegex(content, 'Person Two')
        self.assertRegex(content, 'Person Three')
        self.assertRegex(content, 'Person Four')

    def remove_answer(self, page):
        # Add first person
        form_data = MultiDict()
        form_data.add("first-name", 'Person One')
        form_data.add("first-name_1", 'Person Two')
        form_data.add("first-name_2", 'Person Three')
        form_data.add("first-name_3", '')
        form_data.add("action[remove_answer]", "1") # Remove person two.
        resp = self.client.post(page, data=form_data, follow_redirects=False)

        self.assertEquals(resp.status_code, 200)

        resp = self.navigate_to_page(page)
        content = resp.get_data(True)
        self.assertRegex(content, 'first-name')
        self.assertRegex(content, 'first-name_2')
        self.assertRegex(content, 'first-name_3')

        self.assertNotRegex(content, 'first-name_1')

    def add_answers(self):
        self.login_and_check_introduction_text()
        first_page = self.start_questionnaire()

        # Add first person
        form_data = MultiDict()
        form_data.add("first-name", 'Person One')
        form_data.add("action[add_answer]", "")
        resp = self.client.post(first_page, data=form_data, follow_redirects=False)

        self.assertEquals(resp.status_code, 200)

        resp = self.navigate_to_page(first_page)
        content = resp.get_data(True)
        self.assertRegex(content, 'first-name_1')

        # Add second person
        form_data = MultiDict()
        form_data.add("first-name", 'Person One')
        form_data.add("first_1", 'Person Two')
        form_data.add("action[add_answer]", "")
        resp = self.client.post(first_page, data=form_data, follow_redirects=False)

        self.assertEquals(resp.status_code, 200)

        resp = self.navigate_to_page(first_page)
        content = resp.get_data(True)
        self.assertRegex(content, 'first-name_1')
        self.assertRegex(content, 'first-name_2')

        # Add third person
        form_data = MultiDict()
        form_data.add("first-name", 'Person One')
        form_data.add("first-name_1", 'Person Two')
        form_data.add("first-name_2", 'Person Three')
        form_data.add("action[add_answer]", "")
        resp = self.client.post(first_page, data=form_data, follow_redirects=False)

        self.assertEquals(resp.status_code, 200)

        resp = self.navigate_to_page(first_page)
        content = resp.get_data(True)
        self.assertRegex(content, 'first-name_1')
        self.assertRegex(content, 'first-name_2')
        self.assertRegex(content, 'first-name_3')

        return first_page

    def login_and_check_introduction_text(self):
        self.token = create_token('household_question', 'test')
        resp = self.get_first_page()
        self.check_introduction_text(resp)

    def get_first_page(self):
        resp = self.client.get('/session?token=' + self.token.decode(), follow_redirects=True)
        self.assertEquals(resp.status_code, 200)
        return resp

    def check_introduction_text(self, response):
        content = response.get_data(True)
        self.assertRegex(content, '<li>Household questions.</li>')

    def start_questionnaire(self):
        # Go to questionnaire
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post(self.INTRODUCTION_PAGE, data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        return resp.headers['Location']

    def navigate_to_page(self, page):
        resp = self.client.get(page, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)
        return resp




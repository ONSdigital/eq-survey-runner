from tests.integration.star_wars.star_wars_tests import StarWarsTestCase
from tests.integration.star_wars import star_wars_test_urls

class TestPreviousLink(StarWarsTestCase):

    def test_previous_link_path(self):

        self.login_and_check_introduction_text()

        first_page = self.start_questionnaire_and_navigate_routing()

        introduction = star_wars_test_urls.STAR_WARS_INTRODUCTION

        resp = self.navigate_to_page(introduction)

        self.check_introduction_text(resp)

        # navigate back to first page
        self.navigate_to_page(first_page)

        # Our answers
        form_data = {

            "6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b": "234",
            "92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "40",
            "pre49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "1370",

            "a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d": "Elephant",
            "7587eb9b-f24e-4dc0-ac94-66118b896c10": "Luke, I am your father",
            "9587eb9b-f24e-4dc0-ac94-66117b896c10": "[Luke Skywalker, Yoda, Qui-Gon Jinn]",

            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "28",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "05",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "1983",

            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "29",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "05",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "1983",

            "action[save_continue]": "Save &amp; Continue"
        }

        # Form submission with no errors
        resp = self.submit_page(first_page, form_data)
        self.assertNotEquals(resp.headers['Location'], first_page)

        second_page = resp.headers['Location']

        # go to the second page
        self.check_second_quiz_page(second_page)

        resp = self.client.get(star_wars_test_urls.STAR_WARS_PREVIOUS, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        self.assertEquals(resp.headers['Location'], first_page)

        resp = self.client.get(resp.headers['Location'])

        content = resp.get_data(True)
        self.assertRegexpMatches(content, ">Save &amp; Continue<")
        self.assertRegexpMatches(content, 'Star Wars Quiz')
        self.assertRegexpMatches(content, 'May the force be with you young EQ developer')

        # now go back to the second page
        self.check_second_quiz_page(second_page)

    def test_previous_link_to_introduction(self):

        self.login_and_check_introduction_text()

        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }

        # first start the survey
        resp = self.client.post(star_wars_test_urls.STAR_WARS_INTRODUCTION, data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        self.assertRegexpMatches(resp.headers['Location'], star_wars_test_urls.STAR_WARS_CHOOSE_YOUR_SIDE_REGEX)

        # then click previous
        resp = self.client.get(star_wars_test_urls.STAR_WARS_PREVIOUS, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        self.assertRegexpMatches(resp.headers['Location'], star_wars_test_urls.STAR_WARS_INTRODUCTION_REGEX)

        # then try to start the survey again
        resp = self.client.post(star_wars_test_urls.STAR_WARS_INTRODUCTION, data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        self.assertRegexpMatches(resp.headers['Location'], star_wars_test_urls.STAR_WARS_CHOOSE_YOUR_SIDE_REGEX)



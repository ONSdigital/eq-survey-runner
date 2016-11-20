from tests.integration.star_wars.star_wars_tests import StarWarsTestCase
from werkzeug.datastructures import MultiDict
from tests.integration.star_wars import star_wars_test_urls


class TestNavigation(StarWarsTestCase):

    def test_light_side_path(self):

        self.login_and_check_introduction_text()

        first_page = self.start_questionnaire_and_navigate_routing()

        introduction = star_wars_test_urls.STAR_WARS_INTRODUCTION

        resp = self.navigate_to_page(introduction)

        self.check_introduction_text(resp)

        # navigate back to first page
        self.navigate_to_page(first_page)

        # Our answers
        form_data = MultiDict()
        # Start Date
        form_data.add("6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b", "234")
        form_data.add("92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c", "40")
        form_data.add("pre49d93-cbdc-4bcb-adb2-0e0af6c9a07c", "1370")

        form_data.add("a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d", "Elephant")
        form_data.add("7587eb9b-f24e-4dc0-ac94-66118b896c10", "Luke, I am your father")

        # Check three boxes
        form_data.add("9587eb9b-f24e-4dc0-ac94-66117b896c10", 'Luke Skywalker')
        form_data.add("9587eb9b-f24e-4dc0-ac94-66117b896c10", 'Yoda')
        form_data.add("9587eb9b-f24e-4dc0-ac94-66117b896c10", 'Qui-Gon Jinn')

        form_data.add("6fd644b0-798e-4a58-a393-a438b32fe637-day", "28")
        form_data.add("6fd644b0-798e-4a58-a393-a438b32fe637-month", "05")
        form_data.add("6fd644b0-798e-4a58-a393-a438b32fe637-year", "1983")
        # End Date
        form_data.add("06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day", "29")
        form_data.add("06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month", "05")
        form_data.add("06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year", "1983")

        # User Action
        form_data.add("action[save_continue]", "Save &amp; Continue")

        # Form submission with no errors
        resp = self.submit_page(first_page, form_data)
        self.assertNotEquals(resp.headers['Location'], first_page)

        second_page = resp.headers['Location']

        # go to the second page
        self.check_second_quiz_page(second_page)

        # now navigate back to the first page
        self.check_quiz_first_page(first_page)

        # now go back to the second page
        self.check_second_quiz_page(second_page)

        # Our answers
        form_data = {
            # People in household
            "215015b1-f87c-4740-9fd4-f01f707ef558": "Wookiees don’t place value in material rewards and refused the medal initially",  # NOQA
            "7587qe9b-f24e-4dc0-ac94-66118b896c10": "Yes",
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.submit_page(second_page, form_data)

        # third page
        third_page = resp.headers['Location']
        resp = self.navigate_to_page(third_page)
        content = resp.get_data(True)

        self.assertRegexpMatches(content, "Finally, which  is your favourite film?")

        form_data = {
          # final answers
          "fcf636ff-7b3d-47b6-aaff-9a4b00aa888b": "Naboo",
          "4a085fe5-6830-4ef6-96e6-2ea2b3caf0c1": "5",
          # User Action
          "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.submit_page(third_page, form_data)

        # There are no validation errors
        self.assertRegexpMatches(resp.headers['Location'], star_wars_test_urls.STAR_WARS_SUMMARY_REGEX)

        summary_url = resp.headers['Location']

        resp = self.navigate_to_page(summary_url)

        # We are on the review answers page
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '<title>Summary</title>')
        self.assertRegexpMatches(content, '>Star Wars</')
        self.assertRegexpMatches(content, '>Your responses<')
        self.assertRegexpMatches(content, '(?s)How old is Chewy?.*?234')
        self.assertRegexpMatches(content, '(?s)How many Octillions do Nasa reckon it would cost to build a death star?.*?£40')
        self.assertRegexpMatches(content, '(?s)How hot is a lightsaber in degrees C?.*?1370')
        self.assertRegexpMatches(content, '(?s)What animal was used to create the engine sound of the Empire\'s TIE fighters?.*?Elephant')  # NOQA
        self.assertRegexpMatches(content, '(?s)Which of these Darth Vader quotes is wrong?.*?Luke, I am your father')
        self.assertRegexpMatches(content, '(?s)Which 3 have wielded a green lightsaber?.*?Yoda')  # NOQA
        self.assertRegexpMatches(content, '(?s)Which 3 appear in any of the opening crawlers?')
        self.assertRegexpMatches(content, '(?s)When was The Empire Strikes Back released?.*?28 May 1983 to 29 May 1983')  # NOQA
        self.assertRegexpMatches(content, '(?s)What was the total number of Ewokes?.*?')
        self.assertRegexpMatches(content, '(?s)Why doesn\'t Chewbacca receive a medal at the end of A New Hope?.*?Wookiees don’t place value in material rewards and refused the medal initially')  # NOQA
        self.assertRegexpMatches(content, '>Please check carefully before submission.<')
        self.assertRegexpMatches(content, '>Submit answers<')

        self.complete_survey(summary_url, 'star_wars')

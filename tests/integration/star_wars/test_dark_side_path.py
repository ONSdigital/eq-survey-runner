from tests.integration.navigation import navigate_to_page
from tests.integration.star_wars import BLOCK_2_DEFAULT_ANSWERS
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestDarkSidePath(StarWarsTestCase):

    def test_dark_side_path_no_errors(self):
        self.login()
        first_page = self.start_questionnaire_and_navigate_routing()

        # Submit form with no errors
        resp = self.submit_page(first_page, BLOCK_2_DEFAULT_ANSWERS)
        self.assertNotEqual(resp.location, first_page)

        # Second page
        second_page = resp.location
        resp = navigate_to_page(self.client, second_page)

        content = resp.get_data(True)

        # Make sure we are on the next page
        self.assertRegex(content, 'What was the total number of Ewoks?')
        self.assertRegex(content, 'jar-jar-binks-answer')

    def test_mandatory_currency_should_raise_error(self):
        self.login()
        first_page = self.start_questionnaire_and_navigate_routing()
        # Testing Currency  - Mandatory
        form_data = {
            "chewies-age-answer": "430",
            "death-star-cost-answer": "",
            "lightsaber-cost-answer": "",

            "tie-fighter-sound-answer": "Elephant",
            "green-lightsaber-answer": ['Luke Skywalker', 'Yoda', 'Qui-Gon Jinn'],

            "empire-strikes-back-from-answer-day": "1",
            "empire-strikes-back-from-answer-month": "1",
            "empire-strikes-back-from-answer-year": "2016",

            "empire-strikes-back-to-answer-day": "1",
            "empire-strikes-back-to-answer-month": "1",
            "empire-strikes-back-to-answer-year": "2017",

            "action[save_continue]": "Save &amp; Continue"
        }

        # Submit the form
        resp = self.submit_page(first_page, form_data)
        # Test error messages
        content = resp.get_data(True)
        self.assertRegex(content, 'This field is mandatory.')
        return first_page

    def test_date_range_validation(self):
        self.login()
        first_page = self.start_questionnaire_and_navigate_routing()
        form_data = {
            "chewies-age-answer": "430",
            "death-star-cost-answer": "10",
            "lightsaber-cost-answer": "",

            "tie-fighter-sound-answer": "Elephant",
            "green-lightsaber-answer": ['Luke Skywalker', 'Yoda', 'Qui-Gon Jinn'],

            "empire-strikes-back-from-answer-day": "1",
            "empire-strikes-back-from-answer-month": "1",
            "empire-strikes-back-from-answer-year": "2016",

            "empire-strikes-back-to-answer-day": "1",
            "empire-strikes-back-to-answer-month": "1",
            "empire-strikes-back-to-answer-year": "2015",

            "action[save_continue]": "Save &amp; Continue"
        }
        # Submit the form
        resp = self.submit_page(first_page, form_data)
        # Test error messages
        content = resp.get_data(True)
        self.assertRegex(content, 'The &#39;period to&#39; date cannot be before the &#39;period from&#39; date.')
        return first_page

    def test_negative_currency(self):
        self.login()
        first_page = self.start_questionnaire_and_navigate_routing()
        form_data = {
            "chewies-age-answer": "430",
            "death-star-cost-answer": "-10",
            "lightsaber-cost-answer": "",

            "tie-fighter-sound-answer": "Elephant",
            "green-lightsaber-answer": ['Luke Skywalker', 'Yoda', 'Qui-Gon Jinn'],

            "empire-strikes-back-from-answer-day": "1",
            "empire-strikes-back-from-answer-month": "1",
            "empire-strikes-back-from-answer-year": "2015",

            "empire-strikes-back-to-answer-day": "1",
            "empire-strikes-back-to-answer-month": "1",
            "empire-strikes-back-to-answer-year": "2016",

            "action[save_continue]": "Save &amp; Continue"
        }

        # Submit the form
        resp = self.submit_page(first_page, form_data)
        # Test error messages
        content = resp.get_data(True)
        self.assertRegex(content, 'How can it be negative?')
        return first_page

    def test_validation_combination(self):
        """
            Testing
                   Integer  - Mandatory
                            - Negative
                   Currency - To large
                   Date     - From and to the same
        """
        self.login()
        first_page = self.start_questionnaire_and_navigate_routing()
        form_data = {
            "chewies-age-answer": "",
            "death-star-cost-answer": "9999999999999",
            "lightsaber-cost-answer": "-5",

            "tie-fighter-sound-answer": "Elephant",
            "green-lightsaber-answer": ['Luke Skywalker', 'Yoda', 'Qui-Gon Jinn'],

            "empire-strikes-back-from-answer-day": "1",
            "empire-strikes-back-from-answer-month": "1",
            "empire-strikes-back-from-answer-year": "2016",

            "empire-strikes-back-to-answer-day": "1",
            "empire-strikes-back-to-answer-month": "1",
            "empire-strikes-back-to-answer-year": "2016",

            "action[save_continue]": "Save &amp; Continue"
        }
        # Submit the form
        resp = self.submit_page(first_page, form_data)
        # Test error messages
        content = resp.get_data(True)
        self.assertRegex(content, 'This field is mandatory')
        self.assertRegex(content, 'How much, idiot you must be')
        self.assertRegex(content, 'How can it be negative?')
        self.assertRegex(content, 'The &#39;period to&#39; date must be different to the &#39;period from&#39; date.')
        return first_page

    def test_more_validation_combinations(self):
        """
            Testing
                   Integer     - To large
                               - Not Integer
                   Currency    - Not Integer
                   Radio boxes - Mandatory
                   Checkboxes  - Mandatory
                   Date        - Invalid (empty)
                               - Invalid (Bad date)
        """
        self.login()
        first_page = self.start_questionnaire_and_navigate_routing()
        form_data = {
            "chewies-age-answer": "555555555555555555",
            "death-star-cost-answer": "text",
            "lightsaber-cost-answer": "###",

            "tie-fighter-sound-answer": "",
            "darth-vader-quotes-answer": "",
            "green-lightsaber-answer": "",

            "empire-strikes-back-from-answer-day": "",
            "empire-strikes-back-from-answer-month": "",
            "empire-strikes-back-from-answer-year": "",

            "empire-strikes-back-to-answer-day": "30",
            "empire-strikes-back-to-answer-month": "2",
            "empire-strikes-back-to-answer-year": "2016",

            "action[save_continue]": "Save &amp; Continue"
        }
        # Submit the form
        resp = self.submit_page(first_page, form_data)
        # Test error messages
        content = resp.get_data(True)
        self.assertRegex(content, 'No one lives that long, not even Yoda')
        self.assertRegex(content, 'Please only enter whole numbers into the field.')
        self.assertRegex(content, 'Please only enter whole numbers into the field.')
        self.assertRegex(content, 'This field is mandatory.')
        self.assertRegex(content, 'This field is mandatory.')
        self.assertRegex(content, 'The date entered is not valid')
        self.assertRegex(content, 'The date entered is not valid')
        return first_page

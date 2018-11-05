from app.validation.error_messages import error_messages
from tests.integration.star_wars import STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestDarkSidePath(StarWarsTestCase):

    def test_dark_side_path_no_errors(self):
        self.launchSurvey()
        self.start_questionnaire_and_navigate_routing()

        # Submit form with no errors
        self.post(STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS)

        # Make sure we are on the next page
        self.assertInUrl('star-wars-trivia-part-2')
        self.assertInBody('What was the total number of Ewoks?')
        self.assertInBody('jar-jar-binks-answer')

    def test_mandatory_currency_should_raise_error(self):
        self.launchSurvey()
        self.start_questionnaire_and_navigate_routing()

        # Testing Currency - remove Mandatory answers
        form_data = STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS.copy()
        del form_data['death-star-cost-answer']
        del form_data['lightsaber-cost-answer']

        # Submit the form
        self.post(form_data)

        # Test error messages
        self.assertInBody('Enter an answer to continue.')

    def test_date_range_validation(self):
        self.launchSurvey()
        self.start_questionnaire_and_navigate_routing()
        form_data = STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS.copy()
        form_data.update({
            # From
            'empire-strikes-back-from-answer-day': '1',
            'empire-strikes-back-from-answer-month': '1',
            'empire-strikes-back-from-answer-year': '2016',
            # To (before from)
            'empire-strikes-back-to-answer-day': '1',
            'empire-strikes-back-to-answer-month': '1',
            'empire-strikes-back-to-answer-year': '2015'
        })
        # Submit the form
        self.post(form_data)
        # Test error messages
        self.assertInBody(str(error_messages['INVALID_DATE_RANGE']))

    def test_negative_currency(self):
        self.launchSurvey()
        self.start_questionnaire_and_navigate_routing()
        form_data = STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS.copy()
        form_data['death-star-cost-answer'] = '-10'  # Negative is invalid
        # Submit the form
        self.post(form_data)
        # Test error messages
        self.assertInBody('How can it be negative?')

    def test_validation_combination(self):
        """
            Testing
                   Integer  - Mandatory
                            - Negative
                   Currency - To large
                   Date     - From and to the same
        """
        self.launchSurvey()
        self.start_questionnaire_and_navigate_routing()
        form_data = STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS.copy()
        form_data.update({
            'chewies-age-answer': '',
            'death-star-cost-answer': '9999999999999',
            'lightsaber-cost-answer': '-5',

            'empire-strikes-back-from-answer-day': '1',
            'empire-strikes-back-from-answer-month': '1',
            'empire-strikes-back-from-answer-year': '2016',

            'empire-strikes-back-to-answer-day': '1',
            'empire-strikes-back-to-answer-month': '1',
            'empire-strikes-back-to-answer-year': '2016'
        })
        # Submit the form
        self.post(form_data)
        # Test error messages
        self.assertInBody(str(error_messages['MANDATORY_NUMBER']))
        self.assertInBody('How much, idiot you must be')
        self.assertInBody('How can it be negative?')
        self.assertInBody(str(error_messages['INVALID_DATE_RANGE']))

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
        self.launchSurvey()
        self.start_questionnaire_and_navigate_routing()
        form_data = {
            'chewies-age-answer': '555555555555555555',
            'death-star-cost-answer': 'text',
            'lightsaber-cost-answer': '###',

            'tie-fighter-sound-answer': '',
            'darth-vader-quotes-answer': '',
            'green-lightsaber-answer': '',

            'empire-strikes-back-from-answer-day': '',
            'empire-strikes-back-from-answer-month': '',
            'empire-strikes-back-from-answer-year': '',

            'empire-strikes-back-to-answer-day': '30',
            'empire-strikes-back-to-answer-month': '2',
            'empire-strikes-back-to-answer-year': '2016'
        }
        # Submit the form
        self.post(form_data)
        # Test error messages
        self.assertInBody('No one lives that long, not even Yoda')
        self.assertInBody(str(error_messages['INVALID_NUMBER']))
        self.assertInBody('Select an answer to continue.')
        self.assertInBody(str(error_messages['MANDATORY_DATE']))

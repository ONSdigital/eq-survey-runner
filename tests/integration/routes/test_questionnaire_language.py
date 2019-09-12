from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireLanguage(IntegrationTestCase):
    """ Tests that the language selection from tokens works """

    def test_load_cy_survey(self):
        # When: load a cy survey
        self.launchSurvey('test_language', language_code='cy')
        # Then: welsh
        self.assertInBody('Rhowch enw')

    def test_load_non_existent_lang_fallback(self):
        # When: load a hindi survey
        self.launchSurvey('test_language', language_code='hi')
        # Then: Falls back to english
        self.assertInBody('First Name')

    def test_language_switch_in_flight(self):
        # load a english survey
        self.launchSurvey('test_language', language_code='en')
        # The language is english
        self.assertInBody('First Name')
        # Switch the language to welsh
        self.get('{}?language_code=cy'.format(self.last_url))
        self.assertInBody('Rhowch enw')

    def test_switch_to_invalid_language(self):
        # load a english survey
        self.launchSurvey('test_language', language_code='en')
        # The language is english
        self.assertInBody('First Name')
        # Try and switch to an invalid language
        self.get('{}?language_code=hi'.format(self.last_url))
        self.assertInBody('First Name')

    def test_title_placeholders_rendered_in_summary_using_correct_language(self):
        self.launchSurvey('test_language')

        self.post({'first-name': 'Kevin', 'last-name': 'Bacon'})
        self.assertInBody('What is Kevin Bacon’s date of birth?')

        self.post(
            {
                'date-of-birth-answer-day': 1,
                'date-of-birth-answer-month': 2,
                'date-of-birth-answer-year': 1999,
            }
        )

        self.assertInUrl('/summary/')
        self.assertInBody('What is Kevin Bacon’s date of birth?')
        self.assertInBody('1 February 1999')

        self.get(self.last_url + '?language_code=cy')

        self.assertInUrl('/summary/?language_code=cy')
        self.assertInBody('Beth yw dyddiad geni Kevin Bacon?')
        self.assertInBody('1 Chwefror 1999')

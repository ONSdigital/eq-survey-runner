from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireLanguage(IntegrationTestCase):
    """ Tests that the language selection from tokens works """
    def test_load_cy_survey(self):
        # When: load a cy survey
        self.launchSurvey('test', 'language', language_code='cy')
        # Then: welsh
        self.assertInBody('Holiadur Cymraeg')

    def test_load_non_existant_lang_fallback(self):
        # When: load a hindi survey
        self.launchSurvey('test', 'language', language_code='hi')
        # Then: Falls back to english
        self.assertInBody('English Questionnaire')

    def test_language_switch_in_flight(self):
        # load a english survey
        self.launchSurvey('test', 'language', language_code='en')
        # The language is english
        self.assertInBody('English Questionnaire')
        # Switch the language to welsh
        self.get('{}?language_code=cy'.format(self.last_url))
        self.assertInBody('Holiadur Cymraeg')

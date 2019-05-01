from tests.integration.integration_test_case import IntegrationTestCase

class TestQuestionnairePiping(IntegrationTestCase):

    def test_given_quotes_in_answer_when_piped_into_page_then_html_escaped_quotes_on_page(self):
        # Given
        self.launchSurvey('test', 'multiple_piping')
        self.post(action='start_questionnaire')
        self.post({'address-line-1': '44 hill side'})
        self.post(action='save_continue')

        # When
        self.post({'first-text': 'Joe', 'second-text': 'Bloggs "Junior"'})
        self.post(action='save_continue')

        # Then
        self.get(self.last_url)
        self.assertStatusOK()
        self.assertInSelector(
            'Does <em>Joe Bloggs "Junior"</em> live at <em>44 hill side</em>',
            '#container-multiple-piping-answer',
        )

    def test_given_backslash_in_answer_when_piped_into_page_then_backslash_on_page(self):
        # Given
        self.launchSurvey('test', 'multiple_piping')
        self.post(action='start_questionnaire')
        self.post({'address-line-1': '44 hill side'})
        self.post(action='save_continue')

        # When
        self.post({'first-text': 'Joe', 'second-text': 'Bloggs\\John Doe'})
        self.post(action='save_continue')

        # Then
        self.get(self.last_url)
        self.assertStatusOK()
        self.assertInSelector(
            'Joe Bloggs\\John Doe',
            '#container-multiple-piping-answer'
        )

    def test_answer_piped_into_option(self):
        # Given
        self.launchSurvey('test', 'multiple_piping')
        self.post(action='start_questionnaire')
        self.post({'address-line-1': '44 hill side', 'town-city': 'newport'})
        self.post(action='save_continue')

        # When
        self.post({'first-text': 'Joe', 'second-text': 'Bloggs\\John Doe'})
        self.post(action='save_continue')

        # Then
        self.get(self.last_url)
        self.assertStatusOK()
        self.assertInSelector(
            '44 hill side, newport',
            '#label-multiple-piping-answer-0'
        )

    def test_answer_piped_into_option_on_validation_error(self):
        """Regression test to assert that the previous answer is still piped into
        the option label on the form it is rendered with a validation error
        """
        # Given
        self.launchSurvey('test', 'multiple_piping')
        self.post(action='start_questionnaire')
        self.post({'address-line-1': '44 hill side', 'town-city': 'newport'})
        self.post(action='save_continue')
        self.post({'first-text': 'Joe', 'second-text': 'Bloggs\\John Doe'})
        self.post(action='save_continue')

        # When
        self.post({})

        # Then
        self.assertStatusOK()
        self.assertInSelector(
            '44 hill side, newport',
            '#label-multiple-piping-answer-0'
        )

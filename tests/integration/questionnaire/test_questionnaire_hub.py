from tests.integration.integration_test_case import IntegrationTestCase

HUB_URL = '/questionnaire/'


class TestQuestionnaireHub(IntegrationTestCase):
    def test_navigation_to_hub_route_when_hub_not_enabled(self):
        # Given the hub is not enabled
        self.launchSurvey('test_checkbox')

        # When I navigate to the hub url
        self.get(HUB_URL)

        # Then I should be redirected to the first incomplete question
        self.assertInBody('Which pizza toppings would you like?')
        self.assertInUrl('mandatory-checkbox')

    def test_invalid_block_id_redirects_to_hub_when_hub_enabled(self):
        # Given the hub is enabled
        self.launchSurvey('test_hub_and_spoke')

        # When I navigate to an invalid block id
        self.get('questionnaire/invalid-block-id/')

        # Then I should be redirected to the hub
        self.assertEqualUrl(HUB_URL)

    def test_redirect_to_hub_when_section_complete(self):
        # Given the hub is enabled
        self.launchSurvey('test_hub_and_spoke')

        # When I complete a section
        self.post(action='submit')
        self.post({'employment-status-answer': 'Working as an employee'})

        # Then I should be redirected to the hub
        self.assertEqualUrl(HUB_URL)

    def test_save_and_sign_out_from_the_hub(self):
        # Given the hub is enabled
        self.launchSurvey('test_hub_and_spoke')

        # When I click Save and sign out
        self.post(action='save_sign_out')

        # Then I should be redirected to the hub
        self.assertEqualUrl('/signed-out')

    def test_survey_submission_from_hub(self):
        # Given the hub is enabled
        self.launchSurvey('test_hub_and_spoke')

        # When I submit the survey
        self.post(action='submit')
        self.post({'employment-status-answer': 'Working as an employee'})
        self.post(action='submit')
        self.post({})
        self.post(action='submit')
        self.post(action='submit')

        # Then I should see the thank you page
        self.assertEqualUrl('/submitted/thank-you/')

    def test_hub_section_url_when_hub_not_enabled(self):
        # Given the hub is not enabled
        self.launchSurvey('test_checkbox')

        # When I navigate to the url for a hub's section
        self.get('/questionnaire/sections/default-section/')

        # Then I should be redirected to the correct location for that section
        self.assertEqualUrl('/questionnaire/mandatory-checkbox/')

    def test_invalid_section_id_redirects_to_hub_when_hub_enabled(self):
        # Given the hub is enabled
        self.launchSurvey('test_hub_and_spoke')

        # When I navigate to the url for a hub's section that does not exist
        self.get('questionnaire/sections/invalid-section/')

        # Then I should be redirected to the hub
        self.assertInUrl(HUB_URL)

    def test_section_url_when_hub_enabled_and_section_not_started(self):
        # Given the hub is enabled
        self.launchSurvey('test_hub_and_spoke')

        # When I navigate to a url for a hub's section
        self.get('questionnaire/sections/employment-section/')

        # Then I should be redirected to the first incomplete question in the section
        self.assertEqualUrl('/questionnaire/employment-status/')

    def test_hub_section_url_when_hub_enabled_and_section_in_progress(self):
        # Given the hub is enabled and a section is in-progress
        self.launchSurvey('test_hub_and_spoke')
        self.post(action='submit')
        self.post({'employment-status-answer-exclusive': 'None of these apply'})
        self.get(HUB_URL)
        self.assertInBody('Partially completed')
        self.assertEqualUrl(HUB_URL)

        # When I navigate to the url for a hub's section that is in-progress
        self.get('/questionnaire/sections/employment-section/')

        # Then I should be redirected to the last complete question in the section
        self.assertEqualUrl('/questionnaire/employment-status/')

    def test_hub_section_url_when_hub_enabled_and_section_complete(self):
        # Given the hub is enabled and a section is complete
        self.launchSurvey('test_hub_and_spoke')
        self.get('/questionnaire/sections/accommodation-section/')
        self.post({})
        self.post(action='submit')
        self.assertInBody('View answers')
        self.assertEqualUrl(HUB_URL)

        # When I navigate to the url for a hub's section that is complete
        self.get('/questionnaire/sections/accommodation-section/')

        # Then I should be redirected to the last completed question in the section
        self.assertEqualUrl('/questionnaire/accommodation-details-summary/')

    def test_hub_inaccessible_if_sections_required_and_incomplete(self):
        self.launchSurvey('test_hub_complete_sections')

        self.get('/questionnaire/')

        # Redirected to first question to complete
        self.assertEqualUrl('/questionnaire/employment-status/')

    def test_hub_accessible_if_sections_required_and_complete(self):
        self.launchSurvey('test_hub_complete_sections')

        self.post({'employment-status-answer': 'Working as an employee'})
        self.post(action='submit')

        self.get('/questionnaire/')

        self.assertEqualUrl('/questionnaire/')

    def test_hub_displays_repeating_sections_with_valid_urls(self):
        # Given the hub is enabled and a section is complete
        self.launchSurvey('test_repeating_sections_with_hub_and_spoke')
        # Go to first section
        self.post(action='submit')

        # Add a primary person
        self.post({'you-live-here': 'Yes'})
        self.post({'first-name': 'John', 'last-name': 'Doe'})

        # First list collector
        self.post({'anyone-else': 'Yes'})

        self.post({'first-name': 'Anna', 'last-name': 'Doe'})

        # Go to second list collector
        self.post({'anyone-else': 'No'})

        # Submit interstitial page
        self.post(action='submit')

        # Go to visitors
        self.post({'another-anyone-else': 'No'})

        # Visitors
        self.post({'visitors-anyone-else': 'Yes'})

        self.post({'first-name': 'Joe', 'last-name': 'Public'})

        # Go back to hub
        self.post({'visitors-anyone-else': 'No'})

        # Get URLs for sections. This should be replaced and done by asserting
        # that the name of the person is present on the hub once that work is done.
        section_urls = self.getHtmlSoup().find_all(
            'a', class_='summary__button', href=True
        )

        # Go to first section
        first_repeating_section_url = section_urls[1].attrs['href']
        self.get(first_repeating_section_url)
        self.post({'proxy-answer': 'Yes'})

        self.assertInBody('What is <em>John Doe’s</em> date of birth?')

        self.get(HUB_URL)

        # Go to second section
        second_repeating_section_url = section_urls[2].attrs['href']
        self.get(second_repeating_section_url)
        self.post({'proxy-answer': 'Yes'})

        self.assertInBody('What is <em>Anna Doe’s</em> date of birth?')

        # Go to visitors
        visitor_repeating_section_url = section_urls[3].attrs['href']
        self.get(visitor_repeating_section_url)
        self.assertInBody('What is <em>Joe Public’s</em> date of birth?')

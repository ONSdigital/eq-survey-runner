from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireQuestionGuidance(IntegrationTestCase):

    def test_question_guidance(self):
        # Given I launch a questionnaire with various guidance
        self.launchSurvey('test', 'question_guidance')
        self.post(action='start_questionnaire')

        # When I start the survey I am presented with the title guidance correctly
        self.assertInUrl('block-test-guidance-title')

        self.assertInPage('This one has a description but no list')
        self.assertInPage('No list items below this text')
        self.assertInPage('This one has no list or description')
        self.assertInPage('Text question')
        self.assertInPage('<input')

        # When we continue to the next page with combinations of the guidance descriptions
        self.post(action='save_continue')

        # Then I am presented with the description guidance correctly
        self.assertInUrl('block-test-guidance-description')
        self.assertInPage('No title above this text, list below')
        self.assertInPage('>Item Include 1<')
        self.assertInPage('>Item Include 2<')
        self.assertInPage('>Item Include 3<')
        self.assertInPage('>Item Include 4<')
        self.assertInPage('Just description, no title above this text, no list below')
        self.assertInPage('Text question')
        self.assertInPage('<input')

        # When we continue to the next page with combinations of the guidance lists
        self.post(action='save_continue')

        # Then I am presented with the lists guidance correctly
        self.assertInUrl('block-test-guidance-lists')
        self.assertInPage('Title, no description, list follows')
        self.assertInPage('>Item Include 1<')
        self.assertInPage('>Item Include 2<')
        self.assertInPage('>Item Include 3<')
        self.assertInPage('>Item Include 4<')
        self.assertInPage('>List with no title or description 1<')
        self.assertInPage('>List with no title or description 2<')
        self.assertInPage('>List with no title or description 3<')
        self.assertInPage('>List with no title or description 4<')
        self.assertInPage('Text question')
        self.assertInPage('<input')

        # When we continue to the description content guidance page
        self.post(action='save_continue')

        # I can see the description content guidance
        self.assertInUrl('block-test-guidance-content-description')
        self.assertInPage('Test show guidance content description')
        self.assertInPage('Guidance with content description')
        self.assertInPage('Text question')
        self.assertInPage('<input')
        self.assertInPage('Show test guidance.')
        self.assertInPage('The text here is for description')

        # When we continue to the title content guidance page
        self.post(action='save_continue')

        # I can see the title content guidance
        self.assertInUrl('block-test-guidance-content-title')
        self.assertInPage('Test show guidance content title')
        self.assertInPage('Guidance with content title')
        self.assertInPage('Text question')
        self.assertInPage('<input')
        self.assertInPage('Show test guidance.')
        self.assertInPage('The text here is for a title')

        # When we continue to the list content guidance page
        self.post(action='save_continue')

        # I can see the list content guidance
        self.assertInUrl('block-test-guidance-content-list')
        self.assertInPage('Test show guidance content list')
        self.assertInPage('Guidance with content list')
        self.assertInPage('Text question')
        self.assertInPage('<input')
        self.assertInPage('Show test guidance.')
        self.assertInPage('The text here is for a list')
        self.assertInPage('Another list item')
        self.assertInPage('One more')

        # When we continue to the test all guidance page
        self.post(action='save_continue')

        # When we navigate to the block with all guidance features enabled
        # Then we are presented with the question guidance with all features enabled
        self.assertInUrl('block-test-guidance-all')

        self.assertInPage('Test guidance all')
        self.assertInPage('>Include<')
        self.assertInPage('>Item Include 1<')
        self.assertInPage('>Item Include 2<')
        self.assertInPage('>Item Include 3<')
        self.assertInPage('>Item Include 4<')

        self.assertInPage('>Exclude<')
        self.assertInPage('>Item Exclude 1<')
        self.assertInPage('>Item Exclude 2<')
        self.assertInPage('>Item Exclude 3<')
        self.assertInPage('>Item Exclude 4<')

        self.assertInPage('>Other<')
        self.assertInPage('>Item Other 1<')
        self.assertInPage('>Item Other 2<')
        self.assertInPage('>Item Other 3<')
        self.assertInPage('>Item Other 4<')

        self.assertInPage('Guidance <b>include</b> description text')
        self.assertInPage('Guidance <b>exclude</b> description text')
        self.assertInPage('Guidance <b>other</b> description text')
        self.assertInPage('Text question')
        self.assertInPage('<input')

        # When we continue we go to the summary page
        self.post(action='save_continue')
        self.assertInUrl('summary')

        # And Submit my answers
        self.post(action='submit_answers')
        self.assertInUrl('thank-you')

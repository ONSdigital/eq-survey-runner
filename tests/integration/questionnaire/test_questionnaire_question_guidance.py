from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireQuestionGuidance(IntegrationTestCase):

    def test_question_guidance(self):
        # Given I launch a questionnaire with various guidance
        self.launchSurvey('test', 'question_guidance')
        self.post(action='start_questionnaire')

        # When I start the survey I am presented with the title guidance correctly

        self.assertInBody('This one has a description but no list')
        self.assertInBody('No list items below this text')
        self.assertInBody('This one has no list or description')

        # When we continue to the next page with combinations of the guidance descriptions
        self.post(action='save_continue')

        # Then I am presented with the description guidance correctly
        self.assertInBody('No title above this text, list below')
        self.assertInBody('>Item Include 1<')
        self.assertInBody('Just description, no title above this text, no list below')

        # When we continue to the next page with combinations of the guidance lists
        self.post(action='save_continue')

        # Then I am presented with the lists guidance correctly
        self.assertInBody('Title, no description, list follows')
        self.assertInBody('>Item Include 1<')
        self.assertInBody('>Item Include 4<')
        self.assertInBody('>List with no title or description 1<')

        # When we continue to the description content guidance page
        self.post(action='save_continue')

        # I can see the description content guidance
        self.assertInBody('Test show guidance content description')
        self.assertInBody('Guidance with content description')
        self.assertInBody('Show test guidance.')
        self.assertInBody('The text here is for description')

        # When we continue to the title content guidance page
        self.post(action='save_continue')

        # I can see the title content guidance
        self.assertInBody('Test show guidance content title')
        self.assertInBody('Guidance with content title')
        self.assertInBody('Show test guidance.')
        self.assertInBody('The text here is for a title')

        # When we continue to the list content guidance page
        self.post(action='save_continue')

        # I can see the list content guidance
        self.assertInBody('Test show guidance content list')
        self.assertInBody('Guidance with content list')
        self.assertInBody('Show test guidance.')
        self.assertInBody('The text here is for a list')
        self.assertInBody('Another list item')
        self.assertInBody('One more')

        # When we continue to the test all guidance page
        self.post(action='save_continue')

        # When we navigate to the block with all guidance features enabled
        # Then we are presented with the question guidance with all features enabled

        self.assertInBody('Test guidance all')
        self.assertInBody('>Include<')
        self.assertInBody('>Item Include 1<')
        self.assertInBody('>Item Include 4<')

        self.assertInBody('>Exclude<')
        self.assertInBody('>Item Exclude 1<')
        self.assertInBody('>Item Exclude 4<')

        self.assertInBody('>Other<')
        self.assertInBody('>Item Other 1<')
        self.assertInBody('>Item Other 4<')

        self.assertInBody('Guidance <b>include</b> description text')
        self.assertInBody('Guidance <b>exclude</b> description text')
        self.assertInBody('Guidance <b>other</b> description text')

        # When we continue we go to the summary page
        self.post(action='save_continue')
        self.assertInUrl('summary')

        # And Submit my answers
        self.post(action='submit_answers')
        self.assertInUrl('thank-you')

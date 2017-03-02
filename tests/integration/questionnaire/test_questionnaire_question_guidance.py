from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireQuestionGuidance(IntegrationTestCase):

    def test_question_guidance(self):
        # Given I launch a questionnaire with various guidance
        token = create_token('question_guidance', 'test')

        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # When we navigate to the block with all guidance features enabled
        resp = self.get_and_post_with_csrf_token(resp.location, {'action[start_questionnaire]': ''})

        # Then we are presented with the question guidance with all features enabled
        self.assertIn('block-test-guidance-all', resp.location)

        get_resp = self.client.get(resp.location)
        content = get_resp.get_data(True)

        self.assertIn('Test guidance all', content)
        self.assertIn('>Include<', content)
        self.assertIn('>Item Include 1<', content)
        self.assertIn('>Item Include 2<', content)
        self.assertIn('>Item Include 3<', content)
        self.assertIn('>Item Include 4<', content)

        self.assertIn('>Exclude<', content)
        self.assertIn('>Item Exclude 1<', content)
        self.assertIn('>Item Exclude 2<', content)
        self.assertIn('>Item Exclude 3<', content)
        self.assertIn('>Item Exclude 4<', content)

        self.assertIn('>Other<', content)
        self.assertIn('>Item Other 1<', content)
        self.assertIn('>Item Other 2<', content)
        self.assertIn('>Item Other 3<', content)
        self.assertIn('>Item Other 4<', content)

        self.assertIn('Guidance <b>include</b> description text', content)
        self.assertIn('Guidance <b>exclude</b> description text', content)
        self.assertIn('Guidance <b>other</b> description text', content)
        self.assertIn('Text question', content)
        self.assertIn('<input', content)

        # When we continue to the next page with combinations of the guidance title
        resp = self.get_and_post_with_csrf_token(resp.location, {'action[save_continue]': ''})

        # Then I am presented with the title guidance correctly
        self.assertIn('block-test-guidance-title', resp.location)

        get_resp = self.client.get(resp.location)
        content = get_resp.get_data(True)
        self.assertIn('This one has a description but no list', content)
        self.assertIn('No list items below this text', content)
        self.assertIn('This one has no list or description', content)
        self.assertIn('Text question', content)
        self.assertIn('<input', content)

        # When we continue to the next page with combinations of the guidance descriptions
        resp = self.get_and_post_with_csrf_token(resp.location, {'action[save_continue]': ''})

        # Then I am presented with the description guidance correctly
        self.assertIn('block-test-guidance-description', resp.location)

        get_resp = self.client.get(resp.location)
        content = get_resp.get_data(True)
        self.assertIn('No title above this text, list below', content)
        self.assertIn('>Item Include 1<', content)
        self.assertIn('>Item Include 2<', content)
        self.assertIn('>Item Include 3<', content)
        self.assertIn('>Item Include 4<', content)
        self.assertIn('Just description, no title above this text, no list below', content)
        self.assertIn('Text question', content)
        self.assertIn('<input', content)

        # When we continue to the next page with combinations of the guidance lists
        resp = self.get_and_post_with_csrf_token(resp.location, {'action[save_continue]': ''})

        # Then I am presented with the lists guidance correctly
        self.assertIn('block-test-guidance-lists', resp.location)

        get_resp = self.client.get(resp.location)
        content = get_resp.get_data(True)
        self.assertIn('Title, no description, list follows', content)
        self.assertIn('>Item Include 1<', content)
        self.assertIn('>Item Include 2<', content)
        self.assertIn('>Item Include 3<', content)
        self.assertIn('>Item Include 4<', content)
        self.assertIn('>List with no title or description 1<', content)
        self.assertIn('>List with no title or description 2<', content)
        self.assertIn('>List with no title or description 3<', content)
        self.assertIn('>List with no title or description 4<', content)
        self.assertIn('Text question', content)
        self.assertIn('<input', content)

        # And I can continue to the summary page
        resp = self.get_and_post_with_csrf_token(resp.location, {'action[save_continue]': ''})
        self.assertIn('summary', resp.location)

        # And Submit my answers
        resp = self.get_and_post_with_csrf_token(resp.location, {'action[submit_answers]': ''})
        self.assertIn('thank-you', resp.location)

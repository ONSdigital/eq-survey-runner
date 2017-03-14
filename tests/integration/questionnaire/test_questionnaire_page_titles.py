from extraction import Extractor

from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnairePageTitles(IntegrationTestCase):

    def test_should_have_question_in_page_title_when_loading_introduction(self):
        # Given
        token = create_token('final_confirmation', 'test')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)

        # When
        extraction = Extractor().extract(resp.get_data(True))

        # Then
        self.assertEqual(extraction.title, 'Final confirmation to submit')

    def test_should_have_question_in_page_title_when_loading_questionnaire(self):
        # Given
        token = create_token('final_confirmation', 'test')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # When
        resp = self.get_and_post_with_csrf_token(resp.location, follow_redirects=True)
        extraction = Extractor().extract(resp.get_data(True))

        # Then
        self.assertEqual(extraction.title, 'What is your favourite breakfast food - Final confirmation to submit')

    def test_should_have_question_in_page_title_when_loading_confirmation(self):
        # Given
        token = create_token('final_confirmation', 'test')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=False)
        resp = self.get_and_post_with_csrf_token(resp.location, follow_redirects=False)

        # When
        resp = self.get_and_post_with_csrf_token(resp.location, data={'breakfast-answer': ''}, follow_redirects=True)
        extraction = Extractor().extract(resp.get_data(True))

        # Then
        self.assertEqual(extraction.title, 'Submit answers - Final confirmation to submit')

    def test_should_have_question_in_page_title_when_loading_summary(self):
        # Given
        token = create_token('percentage', 'test')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # When
        resp = self.get_and_post_with_csrf_token(resp.location, data={'answer': ''}, follow_redirects=True)
        extraction = Extractor().extract(resp.get_data(True))

        # Then
        self.assertEqual(extraction.title, 'Summary - Percentage Field Demo')

    def test_should_have_survey_in_page_title_when_thank_you(self):
        # Given
        token = create_token('final_confirmation', 'test')
        self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # When
        resp = self.client.get('/questionnaire/test/final_confirmation/789/thank-you', follow_redirects=True)
        extraction = Extractor().extract(resp.get_data(True))

        # Then
        self.assertEqual(extraction.title, 'We\'ve received your answers - Final confirmation to submit')

    def test_should_have_survey_in_page_title_when_sign_out(self):
        # Given
        token = create_token('final_confirmation', 'test')
        self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # When
        resp = self.client.get('/questionnaire/test/final_confirmation/789/signed-out', follow_redirects=True)
        extraction = Extractor().extract(resp.get_data(True))

        # Then
        self.assertEqual(extraction.title, 'Signed out - Final confirmation to submit')

    def test_session_expired_page_title(self):
        """
        Checks https://github.com/ONSdigital/eq-survey-runner/issues/1032
        """
        # Given
        token = create_token('final_confirmation', 'test')
        self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # When
        resp = self.client.get('/questionnaire/test/final_confirmation/789/session-expired', follow_redirects=True)
        extraction = Extractor().extract(resp.get_data(True))

        # Then
        self.assertEqual(extraction.title, 'Session expired')

    def test_should_have_survey_in_page_title_when_error(self):
        # Given
        token = create_token('final_confirmation', 'test')
        self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # When
        resp = self.client.get('/questionnaire/test/final_confirmation/789/non-existent-block', follow_redirects=True)
        extraction = Extractor().extract(resp.get_data(True))

        # Then
        self.assertEqual(extraction.title, 'Error 404')

    def test_should_have_group_title_in_page_title_when_interstitial(self):
        # Given
        token = create_token('interstitial_page', 'test')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=False)
        resp = self.get_and_post_with_csrf_token(resp.location, follow_redirects=False)

        # When
        resp = self.get_and_post_with_csrf_token(resp.location, data={'favourite-breakfast': ''}, follow_redirects=True)
        extraction = Extractor().extract(resp.get_data(True))

        # Then
        self.assertEqual(extraction.title, 'Favourite food - Interstitial Pages')

    def test_html_stripped_from_page_titles(self):
        """
        Checks for https://github.com/ONSdigital/eq-survey-runner/issues/1036
        """
        # Given
        token = create_token('markup', 'test')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)
        # When
        # Then
        extraction = Extractor().extract(resp.get_data(True))
        self.assertEqual(extraction.title, 'This is a title with emphasis - Markup test')

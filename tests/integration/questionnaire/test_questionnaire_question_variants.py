from tests.integration.integration_test_case import IntegrationTestCase

class TestQuestionnaireQuestionVariants(IntegrationTestCase):

    def __init__(self, *args, **kwargs):
        self.proxy_url = None
        super().__init__(*args, **kwargs)

    def test_non_proxy_answer_shows_non_proxy_title(self):
        self.launchSurvey('test', 'variants_question')

        self.complete_first_section(proxy=False)

    def test_proxy_answer_shows_proxy_title(self):
        self.launchSurvey('test', 'variants_question')

        self.complete_first_section(proxy=True)

    def test_summaries_proxy(self):
        self.launchSurvey('test', 'variants_question')

        self.complete_first_section(proxy=True)

        self.post(action='save_continue')

        self.complete_currency_section()

        self.post(action='save_continue')


        self.assertInBody('What age is Linus Torvalds')
        self.assertInBody('Are you Linus Torvalds')

        # Now change an answer which has variants depending on it
        self.get(url=self.proxy_url)
        print(self.getHtmlSoup())
        print('\n\n\n\n\n\n')
        self.assertInBody('No, I am answering on their behalf')

        self.post({'proxy-answer': 'non-proxy'}, url=self.proxy_url)
        print(self.getHtmlSoup())

        self.assertInBody('What is your age')

    def complete_first_section(self, proxy=False):
        self.assertInBody('Who is this questionnaire about')

        self.post({
            'first-name-answer': 'Linus',
            'last-name-answer': 'Torvalds'
        })

        self.assertInBody('Are you <em>Linus Torvalds</em>?')

        proxy_answer = 'proxy' if proxy else 'non-proxy'

        self.proxy_url = self.last_url

        self.post({
            'proxy-answer': proxy_answer
        })

        expected_question = 'What age is <em>Linus Torvalds</em>?' if proxy else 'What is your age?'

        self.assertInBody(expected_question)

        self.post({'age-answer': '49'})

        expected_question = '<em>Linus Torvalds</em> is over 16?' if proxy else 'You are over 16?'
        self.assertInBody(expected_question)

        self.post({'age-confirm-answer': 'Yes'})


    def complete_currency_section(self):
        self.post({
            'currency-answer': 'USD'
        })

        self.post({
            'first-number-answer': 123
        })

        self.post({
            'second-number-answer': 321
        })

        self.assertInBody('$123')
        self.assertInBody('$321')

from tests.integration.integration_test_case import IntegrationTestCase

HTML_CONTENT = '"><b>some html</b>'
ESCAPED_CONTENT = '&#34;&gt;&lt;b&gt;some html&lt;/b&gt;'


class TestQuestionnaireHtmlEscaping(IntegrationTestCase):
    def test_quotes_in_textfield(self):
        self.launchSurvey('test_textfield')
        self.post({'name-answer': HTML_CONTENT})

        self.get('/questionnaire/name-block')

        assert ESCAPED_CONTENT in self.getResponseData()

    def test_quotes_in_textarea(self):
        self.launchSurvey('test_textarea')
        self.post({'answer': HTML_CONTENT})

        self.get('/questionnaire/textarea-block')

        assert ESCAPED_CONTENT in self.getResponseData()

    def test_quotes_in_detail_answer(self):
        self.launchSurvey('test_radio_mandatory_with_mandatory_other')
        self.post(
            {'radio-mandatory-answer': 'Other', 'other-answer-mandatory': HTML_CONTENT}
        )

        self.get('/questionnaire/radio-mandatory')

        assert ESCAPED_CONTENT in self.getResponseData()

    def test_quotes_in_numeric_answers(self):
        testdata = [
            ('test_numbers', 'set-minimum'),
            ('test_currency', 'answer'),
            ('test_percentage', 'answer'),
            ('test_unit_patterns', 'centimetres'),
            ('test_dates', 'date-range-from-answer-day'),
            ('test_dates', 'date-range-from-answer-month'),
            ('test_dates', 'date-range-from-answer-year'),
        ]
        for schema, answer_id in testdata:
            with self.subTest(schema=schema, answer_id=answer_id):
                print(schema)
                self.launchSurvey(schema)
                self.post({answer_id: HTML_CONTENT})

                assert ESCAPED_CONTENT in self.getResponseData()

    def test_summary(self):
        self.launchSurvey('test_textfield')
        self.post({'name-answer': HTML_CONTENT})
        assert ESCAPED_CONTENT in self.getResponseData()

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

    def test_relationships(self):
        self.launchSurvey('test_relationships')
        self.post({'anyone-else': 'Yes'})
        self.post({'first-name': HTML_CONTENT, 'last-name': 'Jones'})
        self.post({'anyone-else': 'Yes'})
        self.post({'first-name': 'Dave', 'last-name': 'Jones'})
        self.post({'anyone-else': 'No'})

        # When the Javascript runs it uses `getAttribute` to get the content from
        # the `data-title` and `data-playback` attributes. Unfortunately this also
        # un-escapes any escaped html, which undoes any escaping applied to rendered
        # placeholders. To make this work we escape the whole attribute string
        # (effectively double escaping rendered placeholders).
        #
        # https://stackoverflow.com/questions/11224362/getattributename-unescapes-html
        # pylint: disable=line-too-long
        assert (
            'data-title="Thinking of &amp;#34;&amp;gt;&amp;lt;b&amp;gt;some html&amp;lt;/b&amp;gt; Jones, Dave Jones is their &lt;em&gt;brother or sister&lt;/em&gt;"'
            in self.getResponseData()
        )
        assert (
            'data-playback="Dave Jones is &amp;#34;&amp;gt;&amp;lt;b&amp;gt;some html&amp;lt;/b&amp;gt; Jones’ &lt;em&gt;brother or sister&lt;/em&gt;"'
            in self.getResponseData()
        )

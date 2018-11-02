from tests.integration.integration_test_case import IntegrationTestCase

class TestHouseholdWhenRouting(IntegrationTestCase):
    """Test repeating repeating answers build up a summary
    using the format_repeating_answers filter
    """
    def setUp(self):
        super().setUp()
        self.launchSurvey('test', 'repeating_answer_summaries',
                          roles=['dumper'])

    def test_names_appear_in_summaries(self):
        """
        Assert that all entered names are shown on each confirmation question
        page.
        """
        form_data = {
            'primary-first-name': 'Joe',
            'primary-middle-names': '',
            'primary-last-name': 'Bloggs'
        }

        self.post(form_data)

        self.assertInBody('Joe Bloggs')

        self.post({'primary-anyone-else': 'Yes'})

        form_data = {
            'repeating-first-name': 'Jonny',
            'repeating-middle-names': '',
            'repeating-last-name': 'Jones'
        }

        self.post(form_data)

        self.assertInBody('Joe Bloggs')
        self.assertInBody('Jonny Jones')

        self.post({'repeating-anyone-else': 'Yes'})

        form_data = {
            'repeating-first-name': 'Jane',
            'repeating-middle-names': 'Mary Sarah',
            'repeating-last-name': 'Davies'
        }

        self.post(form_data)

        self.assertInBody('Joe Bloggs')
        self.assertInBody('Jonny Jones')
        self.assertInBody('Jane Mary Sarah Davies')

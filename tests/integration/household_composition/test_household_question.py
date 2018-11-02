from werkzeug.datastructures import MultiDict

from tests.integration.integration_test_case import IntegrationTestCase


class TestHouseholdQuestion(IntegrationTestCase):

    def setUp(self):
        super().setUp()
        self.launchSurvey('test', 'household_question')
        self.assertInBody('Welcome to the Census Test.')
        self.post(action='start_questionnaire')

    def test_add_answer(self):
        self.add_answers()

    def test_remove_answer(self):
        self.add_answers()
        self.remove_answer()

    def test_save_continue_should_save_answers(self):
        # Add four people
        self.post({
            'household-0-first-name': 'John',
            'household-1-first-name': 'Jane',
            'household-2-first-name': 'Joe',
            'household-3-first-name': 'Bran'
        })

        # Skip next page
        self.post({'household-composition-add-another': 'Yes'})

        # Check content on summary page
        self.assertInBody('John')
        self.assertInBody('Jane')
        self.assertInBody('Joe')
        self.assertInBody('Bran')

    def test_can_return_to_composition_and_add_entries(self):
        self.add_answers()
        self.post({
            'household-0-first-name': 'John',
            'household-1-first-name': 'Jane'
        })

        # Answer no and get directed back a page
        self.post({'household-composition-add-another': 'No'})

        form_data = MultiDict()
        form_data.add('household-0-first-name', 'John')
        form_data.add('household-1-first-name', 'Jane')
        form_data.add('household-2-first-name', 'Joe')
        form_data.add('household-0-middle-names', '')
        form_data.add('household-1-middle-names', '')
        form_data.add('household-2-middle-names', '')
        form_data.add('household-0-last-name', '')
        form_data.add('household-1-last-name', '')
        form_data.add('household-2-last-name', '')
        self.post(post_data=form_data)

        self.assertInBody('household-summary')
        self.assertInBody('John')
        self.assertInBody('Jane')
        self.assertInBody('Joe')

    def test_composition_complete_progresses_to_summary(self):
        self.add_answers()
        self.post({
            'household-0-first-name': 'John',
            'household-1-first-name': 'Jane'
        })
        self.assertInUrl('household-summary')
        self.post({'household-composition-add-another': 'Yes'})
        self.assertInUrl('/summary')

    def test_save_sign_out_with_household_question(self):
        self.add_answers()
        self.post(action='save_sign_out')
        self.assertInBody('Your survey answers have been saved')
        self.assertInUrl('signed-out')

    def remove_answer(self):
        self.post(post_data={
            'household-0-first-name': 'John',
            'household-1-first-name': 'Jane',
            'household-2-first-name': 'Joe',
        },
                  action='remove_answer',
                  action_value='1'  # Remove Jane.
                 )

        self.assertNotInBody('first-name_1')

    def add_answers(self):
        # Add three people
        self.post(
            post_data={
                'household-0-first-name': 'John',
                'household-1-first-name': 'Jane',
                'household-2-first-name': 'Joe'
            },
            action='add_answer'
        )

        self.assertStatusOK()
        self.assertInBody('household-0-first-name')
        self.assertInBody('household-1-first-name')
        self.assertInBody('household-2-first-name')

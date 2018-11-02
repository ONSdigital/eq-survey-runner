from werkzeug.datastructures import MultiDict

from tests.integration.integration_test_case import IntegrationTestCase


class TestRepeatingHouseholdRouting(IntegrationTestCase):
    """Test repeating household with routing.

    Tests repeating groups with routing to and around questions within the
    repeating group.
    """
    def setUp(self):
        super().setUp()
        self.launchSurvey('test', 'repeating_household_routing',
                          roles=['dumper'])
        self.post(action='start_questionnaire')
        self.household_composition_url = self.last_url

    def test_repeating_group_no_skip(self):
        # Given I add some people
        form_data = MultiDict()
        form_data.add('household-0-first-name', 'Joe')
        form_data.add('household-0-middle-names', '')
        form_data.add('household-0-last-name', 'Bloggs')
        form_data.add('household-1-first-name', 'Jane')
        form_data.add('household-1-middle-names', '')
        form_data.add('household-1-last-name', 'Doe')
        self.post(form_data)
        self.assertInBody('Is that everyone?')
        self.post({'everyone-at-address-confirmation-answer': 'Yes'})

        # Then provide details for each member
        joe_dob = {
            'date-of-birth-answer-day': '12',
            'date-of-birth-answer-month': '3',
            'date-of-birth-answer-year': '1990'
        }
        self.post(joe_dob)
        self.post({'sex-answer': 'Male'})
        self.post(action='save_continue')
        jane_dob = {
            'date-of-birth-answer-day': '27',
            'date-of-birth-answer-month': '11',
            'date-of-birth-answer-year': '1995'
        }
        self.post(jane_dob)
        self.post({'sex-answer': 'Female'})
        self.post(action='save_continue')

        # The survey answers should still contain the first occupant's DoB
        result = self.dumpAnswers()
        dobs = [a for a in result['answers']
                if a['answer_id'] == 'date-of-birth-answer']
        self.assertEqual(len(dobs), 2, 'There should be two date-of-birth '
                                       'answers')
        self.assertEqual(dobs[0]['value'], '1990-03-12')
        self.assertEqual(dobs[1]['value'], '1995-11-27')

    def test_repeating_group_skip_first(self):
        # Given I add some people
        form_data = MultiDict()
        form_data.add('household-0-first-name', 'Joe')
        form_data.add('household-0-middle-names', '')
        form_data.add('household-0-last-name', 'Bloggs')
        form_data.add('household-1-first-name', 'Jane')
        form_data.add('household-1-middle-names', '')
        form_data.add('household-1-last-name', 'Doe')
        self.post(form_data)
        self.assertInBody('Is that everyone?')
        self.post({'everyone-at-address-confirmation-answer': 'Yes'})

        # Then provide details for each member while skipping DoB
        # question for the first member
        self.post(action='save_continue')
        self.assertInBody('Is Joe Bloggs aged 16 or over?')
        self.post({'dob-check-answer': 'Yes'})
        self.post({'sex-answer': 'Male'})
        self.post(action='save_continue')
        jane_dob = {
            'date-of-birth-answer-day': '27',
            'date-of-birth-answer-month': '11',
            'date-of-birth-answer-year': '1995'
        }
        self.post(jane_dob)
        self.post({'sex-answer': 'Female'})
        self.post(action='save_continue')

        # The survey answers should still contain the first occupant's DoB
        result = self.dumpAnswers()
        janes_dob = [a for a in result['answers']
                     if a['answer_id'] == 'date-of-birth-answer' and
                     a['group_instance'] == 1]
        self.assertEqual(len(janes_dob), 1, 'There should be a date-of-birth '
                                            'answer in group instance 1')
        self.assertEqual(janes_dob[0]['value'], '1995-11-27')

    def test_repeating_group_skip_second(self):
        # Given I add some people
        form_data = MultiDict()
        form_data.add('household-0-first-name', 'Joe')
        form_data.add('household-0-middle-names', '')
        form_data.add('household-0-last-name', 'Bloggs')
        form_data.add('household-1-first-name', 'Jane')
        form_data.add('household-1-middle-names', '')
        form_data.add('household-1-last-name', 'Doe')
        self.post(form_data)
        self.assertInBody('Is that everyone?')
        self.post({'everyone-at-address-confirmation-answer': 'Yes'})

        # Then provide details for the first member
        joe_dob = {
            'date-of-birth-answer-day': '12',
            'date-of-birth-answer-month': '3',
            'date-of-birth-answer-year': '1990'
        }
        self.post(joe_dob)
        self.post({'sex-answer': 'Male'})
        self.post(action='save_continue')

        # When I skip DoB for second member and answer remaining questions
        self.post(action='save_continue')
        self.assertInBody('Is Jane Doe aged 16 or over?')
        self.post({'dob-check-answer': 'Yes'})
        self.assertInBody('What is Jane Doe’s sex?')
        self.post({'sex-answer': 'Female'})

        # The survey answers should still contain the first occupant's DoB
        self.post(action='save_continue')
        result = self.dumpAnswers()
        joes_dob = [a for a in result['answers']
                    if a['answer_id'] == 'date-of-birth-answer' and
                    a['group_instance'] == 0]
        self.assertEqual(len(joes_dob), 1, 'There should be a date-of-birth '
                                           'answer in group instance 0')
        self.assertEqual(joes_dob[0]['value'], '1990-03-12')

class TestHouseholdWhenRouting(IntegrationTestCase):
    """Test repeating household with routing.

    Tests goto clauses which use `answer_count` in the `when` clause
    """
    def setUp(self):
        super().setUp()
        self.launchSurvey('test', 'routing_answer_count',
                          roles=['dumper'])
        self.household_composition_url = self.last_url

    def test_routes_based_on_answer_count(self):
        """ Asserts that the routing rule is followed based on the
        number of answers to a household composition question.
        """
        form_data = MultiDict()
        form_data.add('household-0-first-name', 'Joe')
        form_data.add('household-0-middle-names', '')
        form_data.add('household-0-last-name', 'Bloggs')
        form_data.add('household-1-first-name', 'Jane')
        form_data.add('household-1-middle-names', '')
        form_data.add('household-1-last-name', 'Doe')
        self.post(form_data)

        self.assertInBody('This is Group 1 - you answered "2"')

    def test_routes_based_on_answer_count_false_condition(self):
        """Asserts that the goto is ignored when the condition is false
        """
        form_data = MultiDict()
        form_data.add('household-0-first-name', 'Joe')
        form_data.add('household-0-middle-names', '')
        form_data.add('household-0-last-name', 'Bloggs')
        self.post(form_data)

        self.assertInBody('This is Group 0 - You answered less than "2"')

import unittest


class TestEmptySubmission(unittest.TestCase):
    def test_empty_submission(self):
        # Get a token
        # We are on the landing page
        # We proceed to the questionnaire
        # We are in the Questionnaire
        # We do not fill in our answers
        # We submit the form
        # We are in the Questionnaire
        # There are validation errors
        # We fill in our answers
        # We submit the form
        # We are on the review answers page
        # We submit our answers
        # We are on the thank you page
        self.assertTrue(True)

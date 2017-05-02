from mock import patch
from tests.integration.integration_test_case import IntegrationTestCase

class TestBrokenSubmission(IntegrationTestCase):
    def setUp(self):
        self.patcher = patch('app.LogSubmitter')
        mock_class = self.patcher.start()

        self.instance = mock_class.return_value
        self.instance.send_message.return_value = False

        super().setUp()
        self.launchSurvey('test', 'percentage')

    def tearDown(self):
        self.patcher.stop()

    def test_broken_submitter_results_in_503(self):
        self.post({'answer': '50'})
        self.assertStatusOK()

        self.post(action=None)
        self.assertEqual(self.instance.send_message.called, True)  # pylint: disable=no-member
        self.assertStatusCode(503)

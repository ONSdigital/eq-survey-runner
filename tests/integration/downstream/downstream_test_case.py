from mock import patch, Mock

from app.submitter.submitter import Submitter
from tests.integration.integration_test_case import IntegrationTestCase


class MyMockSubmitter(Submitter):

    def __init__(self):
        self._message = None
        self._submitted_at = None

    @staticmethod
    def encrypt_message(message):
        return message

    def get_message(self):
        return self._message

    def send_message(self, message, queue):
        self._message = message
        return True


class DownstreamTestCase(IntegrationTestCase):
    """
    Overrides the application SubmitterFactory to provide our own which
    allows the message to be captured and interrogated.
    """
    _submitter = MyMockSubmitter()

    @staticmethod
    def get_submitter():
        return DownstreamTestCase._submitter

    def setUp(self):
        super().setUp()
        self.patcher = patch('app.views.questionnaire.SubmitterFactory')
        submitter_factory = self.patcher.start()
        submitter_factory.get_submitter = Mock(return_value=DownstreamTestCase.get_submitter())

    def tearDown(self):
        self.patcher.stop()
